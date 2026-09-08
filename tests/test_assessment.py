import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('assessment', ROOT/'skills/cyber-audit/scripts/assessment.py')
assessment = importlib.util.module_from_spec(spec)
spec.loader.exec_module(assessment)


class AssessmentTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT/'examples/assessment.json').read_text())

    def test_valid_assessment_can_contain_confirmed_defects(self):
        result = assessment.validate(self.data)
        self.assertTrue(result['valid'],result['errors'])
        self.assertGreater(sum(f['status']=='confirmed' for f in self.data['findings']),0)
        self.assertEqual(result['coverage_counts']['tested'],len(self.data['controls']))

    def test_tested_control_requires_evidence_and_executed_cases(self):
        for change in ('evidence','execution'):
            data=copy.deepcopy(self.data)
            data['controls'][0].pop(change)
            self.assertFalse(assessment.validate(data)['valid'])
        for value in (0,False,-1):
            data=copy.deepcopy(self.data)
            data['controls'][0]['execution']['cases_run']=value
            self.assertFalse(assessment.validate(data)['valid'])

    def test_unknown_evidence_reference_rejected(self):
        self.data['findings'][0]['evidence']=['missing']
        self.assertFalse(assessment.validate(self.data)['valid'])

    def test_duplicate_ids_rejected(self):
        for key in ('evidence','controls','findings'):
            data=copy.deepcopy(self.data)
            data[key].append(copy.deepcopy(data[key][0]))
            self.assertFalse(assessment.validate(data)['valid'])

    def test_confirmation_requires_attempt_to_disprove(self):
        self.data['findings'][0]['attempt_to_disprove']=''
        self.assertFalse(assessment.validate(self.data)['valid'])

    def test_untested_and_inapplicable_controls_need_reasons(self):
        for status in ('not-tested','not-applicable','blocked','partial'):
            data=copy.deepcopy(self.data)
            data['controls'][0]['status']=status
            self.assertFalse(assessment.validate(data)['valid'])
            data['controls'][0]['reason']='The requested runtime was not supplied.'
            self.assertTrue(assessment.validate(data)['valid'])

    def test_retested_requires_correction_evidence_and_passing_execution(self):
        finding=self.data['findings'][0]
        finding['status']='retested'
        self.assertFalse(assessment.validate(self.data)['valid'])
        finding['fix_revision']='synthetic-correction'
        finding['retest']=copy.deepcopy(self.data['controls'][0]['execution'])
        finding['retest']['outcome']='pass'
        finding['retest_evidence']=finding['evidence'][:]
        self.assertTrue(assessment.validate(self.data)['valid'])
        finding['retest']['outcome']='fail'
        self.assertFalse(assessment.validate(self.data)['valid'])

    def test_malformed_records_fail_without_an_exception(self):
        for key,value in [('evidence',[None]),('controls',[[]]),('findings','bad'),('target',[]),('limitations',None)]:
            data=copy.deepcopy(self.data)
            data[key]=value
            self.assertFalse(assessment.validate(data)['valid'])
        self.data['findings'][0].update(status='retested',retest='bad')
        self.assertFalse(assessment.validate(self.data)['valid'])

    def test_example_evidence_hashes_match_delivered_bytes(self):
        for evidence in self.data['evidence']:
            raw=(ROOT/evidence['source']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(),evidence['sha256'])
            result=json.loads(raw)
            for name,sha in result['sha256'].items():
                self.assertEqual(hashlib.sha256((ROOT/'tests/fixtures/review_lab'/name).read_bytes()).hexdigest(),sha)

    def test_lab_reproduces_defects_and_legitimate_controls(self):
        run=subprocess.run([sys.executable,'-I','-B',str(ROOT/'examples/review_lab.py')],
                           capture_output=True,text=True,timeout=10,check=True)
        result=json.loads(run.stdout)
        self.assertEqual(result['case_count'],len(result['results']))
        self.assertEqual(result['failed'],0)
        kinds={r['kind'] for r in result['results']}
        self.assertTrue({'F1','F2','F3','legitimate','denial-control','needs-context-single-use-policy'} <= kinds)
        self.assertTrue(all(r['observed']==r['expected_current_behavior'] for r in result['results']))


if __name__ == '__main__':
    unittest.main()

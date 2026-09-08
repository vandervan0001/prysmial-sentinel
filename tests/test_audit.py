import importlib.util
import json
from pathlib import Path
import tempfile
import subprocess
import sys
import os
import unittest

ROOT = Path(__file__).resolve().parents[1]


def module(name,path):
    spec = importlib.util.spec_from_file_location(name,path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


audit = module('audit',ROOT/'skills/cyber-audit/scripts/audit.py')
installer = module('installer',ROOT/'scripts/install.py')


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self,name,content=''):
        p = self.root/name
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(content)

    def test_stack_routing_from_real_dependency_names(self):
        self.write('package.json',json.dumps({'dependencies':{'next':'1','@modelcontextprotocol/sdk':'1','stripe':'1'}}))
        self.write('web/app.tsx','')
        self.write('.github/workflows/build.yml','')
        inv = audit.inventory(self.root)
        plan = audit.make_plan(inv)
        names = {m['name'] for m in plan['modules']}
        self.assertTrue({'cyber-browser','cyber-mcp','cyber-cicd','cyber-business-logic'} <= names)
        self.assertNotIn('cyber-pentest',names)
        self.assertTrue(all(m['status']=='not-tested' for m in plan['skills']))

    def test_package_scripts_are_not_executed_or_used_for_routing(self):
        marker = self.root/'marker'
        self.write('package.json',json.dumps({'scripts':{'install':'touch '+str(marker)},'description':'langchain electron'}))
        inv = audit.inventory(self.root)
        self.assertFalse(marker.exists())
        self.assertNotIn('ai',inv['signals'])
        self.assertNotIn('desktop',inv['signals'])

    def test_env_value_not_read_or_exported(self):
        secret = 'sentinel-private-value-not-to-display'
        self.write('.env','SECRET='+secret)
        self.write('a.py','')
        self.assertNotIn(secret,json.dumps(audit.inventory(self.root)))

    def test_symlink_files_and_directories_excluded(self):
        self.write('real/a.py','')
        (self.root/'linked').symlink_to(self.root/'real',target_is_directory=True)
        (self.root/'linked.py').symlink_to(self.root/'real/a.py')
        inv = audit.inventory(self.root)
        self.assertEqual(inv['files'],['real/a.py'])
        self.assertIn('linked',inv['excluded_paths'])
        self.assertIn('linked.py',inv['excluded_paths'])

    def test_file_limit_marks_partial(self):
        self.write('a.py')
        self.write('b.py')
        inv = audit.inventory(self.root,1)
        self.assertEqual(inv['status'],'partial')
        self.assertEqual(inv['files_seen'],1)

    def test_invalid_manifest_does_not_report_complete(self):
        self.write('package.json','{')
        self.assertEqual(audit.inventory(self.root)['status'],'partial')

    def test_empty_tree_is_not_successful_coverage(self):
        self.assertEqual(audit.inventory(self.root)['status'],'empty')

    def test_manual_ot_routing_and_unknown_rejection(self):
        inv = audit.inventory(self.root)
        plan = audit.make_plan(inv,extra=['cyber-ot'])
        self.assertIn('cyber-ot',{s['name'] for s in plan['skills']})
        self.assertIn('cyber-ot',{s['name'] for s in plan['modules']})
        with self.assertRaises(ValueError): audit.make_plan(inv,extra=['cyber-unknown'])

    def test_dry_scan_has_no_output_side_effect(self):
        self.write('a.py')
        dest = self.root/'result'
        plan = audit.scan_local(self.root,dest)
        self.assertFalse(plan['execute'])
        self.assertFalse(dest.exists())


class EvidenceTests(unittest.TestCase):
    def semgrep(self,results=None,errors=None,scanned=None):
        return {'results':results or [],'errors':errors or [],'paths':{'scanned':scanned or []}}

    def test_semgrep_complete_requires_nonzero_targets(self):
        empty = audit.normalize(self.semgrep(),'semgrep','hash')
        full = audit.normalize(self.semgrep(scanned=['a.py']),'semgrep','hash')
        self.assertEqual(empty['scan_status'],'no-targets')
        self.assertEqual(full['scan_status'],'complete')
        self.assertEqual(full['analyzed_targets'],1)

    def test_semgrep_errors_survive_empty_result(self):
        result = audit.normalize(self.semgrep(errors=[{'message':'private'}],scanned=['a.py']),'semgrep','hash')
        self.assertEqual(result['scan_status'],'partial')
        self.assertNotIn('private',json.dumps(result))

    def test_semgrep_unknown_coverage_stays_unknown(self):
        self.assertEqual(audit.normalize({'results':[]},'semgrep','hash')['scan_status'],'unknown')

    def test_results_are_candidates_and_snippets_omitted(self):
        rows = [{'check_id':'rule','path':'app.py','start':{'line':3},
                 'extra':{'severity':'ERROR','lines':'sentinel-secret','message':'sentinel-secret'}}]
        result = audit.normalize(self.semgrep(results=rows,scanned=['app.py']),'semgrep','hash')
        self.assertEqual(result['findings'][0]['status'],'candidate')
        self.assertNotIn('sentinel-secret',json.dumps(result))

    def test_dedup_preserves_occurrences_and_distinct_locations(self):
        rows = [{'check_id':'rule','path':'app.py','start':{'line':line}} for line in [3,3,8]]
        result = audit.normalize(self.semgrep(results=rows),'semgrep','hash')
        self.assertEqual(result['candidate_count'],2)
        self.assertEqual([r['occurrences'] for r in result['findings']],[2,1])

    def test_sarif_failed_execution_is_visible(self):
        raw = {'version':'2.1.0','runs':[{'tool':{'driver':{'name':'Scanner'}},
                'invocations':[{'executionSuccessful':False}],'results':[]}]}
        self.assertEqual(audit.normalize(raw,'sarif','hash')['scan_status'],'partial')

    def test_sarif_resolves_rule_and_artifact_indices(self):
        raw = {'version':'2.1.0','runs':[{'tool':{'driver':{'name':'CodeQL','rules':[{'id':'r1'}]}},
            'artifacts':[{'location':{'uri':'src/a.py'}}],
            'results':[{'ruleIndex':0,'locations':[{'physicalLocation':{'artifactLocation':{'index':0},'region':{'startLine':9}}}]}]}]}
        row = audit.normalize(raw,'sarif','hash')['findings'][0]
        self.assertEqual((row['rule'],row['path'],row['line']),('r1','src/a.py',9))

    def test_sarif_success_is_not_proof_of_coverage(self):
        raw = {'version':'2.1.0','runs':[{'invocations':[{'executionSuccessful':True}]}]}
        self.assertEqual(audit.normalize(raw,'sarif','hash')['scan_status'],'unknown')

    def test_gitleaks_never_imports_secret_or_match(self):
        raw = [{'RuleID':'token','File':'a.env','StartLine':1,'Secret':'sentinel-secret','Match':'sentinel-secret'}]
        result = audit.normalize(raw,'gitleaks','hash')
        self.assertNotIn('sentinel-secret',json.dumps(result))
        self.assertEqual(result['scan_status'],'unknown')

    def test_gitleaks_distinct_commits_are_not_merged(self):
        raw=[{'RuleID':'token','File':'a.env','StartLine':1,'Commit':c*40} for c in ('a','b')]
        self.assertEqual(audit.normalize(raw,'gitleaks','hash')['candidate_count'],2)

    def test_trivy_empty_does_not_imply_success(self):
        self.assertEqual(audit.normalize({'SchemaVersion':2},'trivy','hash')['scan_status'],'unknown')

    def test_trivy_vulnerability_config_secret_and_nonfinding(self):
        raw = {'SchemaVersion':2,'Results':[{'Target':'Dockerfile','Vulnerabilities':[{'VulnerabilityID':'CVE-fixture','PkgName':'p','InstalledVersion':'1','Severity':'HIGH'}],
                'Misconfigurations':[{'ID':'bad','Status':'FAIL'},{'ID':'good','Status':'PASS'}],
                'Secrets':[{'RuleID':'secret','Match':'sentinel-secret'}]}]}
        result = audit.normalize(raw,'trivy','hash')
        self.assertEqual(result['candidate_count'],3)
        self.assertNotIn('sentinel-secret',json.dumps(result))

    def test_unrecognized_formats_rejected(self):
        for fmt,raw in [('semgrep',{}),('sarif',{'version':'1','runs':[]}),('trivy',{}),('gitleaks',{})]:
            with self.subTest(fmt=fmt),self.assertRaises(ValueError): audit.normalize(raw,fmt,'hash')

    def test_url_credentials_and_queries_not_retained(self):
        self.assertEqual(audit.location('https://user:secret@example.invalid/file?token=secret'),'[remote location omitted]')
        self.assertEqual(audit.location('src/file.py?token=secret'),'src/file.py')

    def test_report_does_not_render_untrusted_html(self):
        raw = [{'RuleID':'<script>x</script>','File':'a|b','StartLine':1}]
        rendered = audit.report(audit.normalize(raw,'gitleaks','hash'))
        self.assertNotIn('<script>',rendered)
        self.assertIn('&lt;script&gt;',rendered)
        self.assertIn('a&#124;b',rendered)

    def test_report_does_not_activate_markdown_links(self):
        raw=[{'RuleID':'[open](file:///private)','File':'a.env','StartLine':1}]
        rendered=audit.report(audit.normalize(raw,'gitleaks','hash'))
        self.assertNotIn('[open]',rendered)

    @unittest.skipUnless(os.name=='posix','process-group timeout applies to POSIX')
    def test_timeout_kills_scanner_children(self):
        # Child inherits the stdout pipe. communicate cannot return until the group dies.
        script='import subprocess,sys,time; subprocess.Popen([sys.executable,"-c","import time; time.sleep(20)"]); print("started",flush=True); time.sleep(20)'
        out,err,rc=audit.run_bounded([sys.executable,'-c',script],ROOT,os.environ.copy(),0.3)
        self.assertIsNone(rc)
        self.assertIn(b'started',out)

    def test_exclusive_evidence_write_and_symlink_rejection(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)/'evidence'
            audit.private_write(p,'first')
            with self.assertRaises(FileExistsError): audit.private_write(p,'second')
            self.assertEqual(p.read_text(),'first')
            link = Path(tmp)/'link'
            link.symlink_to(p)
            with self.assertRaises(ValueError): audit.read_regular(link)


class InstallTests(unittest.TestCase):
    def test_preview_changes_nothing_and_apply_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp)/'skills'
            self.assertEqual(installer.install(dest)['status'],'preview')
            self.assertFalse(dest.exists())
            result = installer.install(dest,True)
            self.assertEqual(result['status'],'installed')
            self.assertTrue((dest/'cyber-audit/SKILL.md').is_file())
            again = installer.install(dest,True)
            self.assertTrue(all(s['status']=='already-linked' for s in again['skills']))

    def test_collision_prevents_all_new_links(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp)
            original = dest/'cyber-audit'
            original.mkdir()
            (original/'mine').write_text('keep')
            result = installer.install(dest,True)
            self.assertEqual(result['status'],'blocked-by-collision')
            self.assertEqual(list(dest.iterdir()),[original])
            self.assertEqual((original/'mine').read_text(),'keep')


if __name__ == '__main__':
    unittest.main()

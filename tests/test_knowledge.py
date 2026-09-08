import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    obj=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


knowledge=load('knowledge',ROOT/'skills/cyber-core/scripts/knowledge.py')
compiler=load('compiler',ROOT/'scripts/compile_controls.py')
attack_builder=load('attack_builder',ROOT/'scripts/build_attack_index.py')


class KnowledgeTests(unittest.TestCase):
    def test_attack_import_preserves_active_techniques_and_relationships(self):
        bundle={'type':'bundle','objects':[
            {'type':'attack-pattern','id':'attack-pattern--one','name':'Active','external_references':[{'source_name':'mitre-attack','external_id':'T9999'}]},
            {'type':'attack-pattern','id':'attack-pattern--old','revoked':True},
            {'type':'attack-pattern','id':'attack-pattern--deprecated','x_mitre_deprecated':True},
            {'type':'relationship','id':'relationship--one','relationship_type':'mitigates','source_ref':'course-of-action--one','target_ref':'attack-pattern--one'}]}
        result=attack_builder.transform(bundle,'ics-attack')
        self.assertEqual(len(result),2)
        self.assertEqual(result[0]['attack_id'],'T9999')
        self.assertEqual(result[1]['relationship_type'],'mitigates')

    def test_attack_import_without_techniques_is_incomplete(self):
        with self.assertRaises(ValueError): attack_builder.transform({'type':'bundle','objects':[]},'ics-attack')

    def test_exact_technique_does_not_select_subtechniques(self):
        result=knowledge.search_attack('T1059','enterprise-attack')
        self.assertEqual(result['matches_total'],1)
        self.assertEqual(result['results'][0]['attack_id'],'T1059')
        self.assertGreater(result['results'][0]['relations_total'],0)

    def test_known_ics_technique_and_nonexistent_control(self):
        result=knowledge.search_attack('Modify Controller Tasking','ics-attack')
        self.assertGreater(result['matches_total'],0)
        self.assertTrue(all(r['domain']=='ics-attack' for r in result['results']))
        self.assertEqual(knowledge.search_attack('SYNTHETIC-NO-SUCH-TECHNIQUE')['matches_total'],0)

    def test_empty_attack_query_rejected(self):
        with self.assertRaises(ValueError): knowledge.search_attack(' ')

    def test_protocol_filter_has_positive_and_negative_controls(self):
        result=knowledge.search_controls('cyber-ot','modbus')
        self.assertGreater(result['count'],0)
        self.assertTrue(all('modbus' in c['applies_to']['protocols'] for c in result['controls']))
        self.assertEqual(knowledge.search_controls('cyber-appsec','modbus')['count'],0)
        self.assertEqual(knowledge.search_controls(protocol='unknown-protocol')['count'],0)

    def test_every_domain_has_structured_controls(self):
        for domain in ['cyber-core','cyber-pentest','cyber-appsec','cyber-detection','cyber-hunting','cyber-purple-team','cyber-dfir','cyber-ot']:
            with self.subTest(domain=domain): self.assertGreater(knowledge.search_controls(domain)['count'],0)

    def test_compiled_corpus_matches_authored_sources(self):
        compiled=compiler.compile_records()
        stored=json.loads((ROOT/'skills/cyber-core/references/controls.json').read_text())
        self.assertEqual(compiled,stored)

    def test_control_validation_rejects_missing_proof_and_duplicate(self):
        record=copy.deepcopy(knowledge.search_controls('cyber-ot','modbus')['controls'][0])
        self.assertEqual(compiler.validate_records([record]),[])
        record['verification']['acceptance']=''
        self.assertTrue(compiler.validate_records([record]))
        record['verification']['acceptance']='proof'
        self.assertTrue(compiler.validate_records([record,record]))

    def test_control_validation_rejects_loss_of_ot_boundary(self):
        record=copy.deepcopy(knowledge.search_controls('cyber-ot','modbus')['controls'][0])
        record['safety']['production_ot']=False
        self.assertTrue(compiler.validate_records([record]))

    def test_catalog_module_identity_matches_path(self):
        data=json.loads((ROOT/'skills/cyber-audit/references/catalog.json').read_text())
        for m in data['modules']:
            self.assertEqual(m['module'],Path(m['path']).stem)
            self.assertEqual(m['name'],'cyber-'+m['module'])


if __name__=='__main__': unittest.main()

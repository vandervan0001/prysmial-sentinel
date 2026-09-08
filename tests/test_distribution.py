import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load('distribution_validator', ROOT/'scripts/validate_library.py')
packager = load('distribution_packager', ROOT/'scripts/package_library.py')


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)/'metadata'
        for relative in ('VERSION', '.claude-plugin/plugin.json', '.claude-plugin/marketplace.json',
                         'skills/cyber-audit/references/repositories.json',
                         'skills/cyber-core/references/attack/provenance.json'):
            target = self.root/relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT/relative, target)
        self.assertEqual(validator.distribution_errors(self.root), [])

    def rewrite(self, relative, change):
        path = self.root/relative
        data = json.loads(path.read_text())
        change(data)
        path.write_text(json.dumps(data))

    def test_plugin_version_drift_is_rejected(self):
        self.rewrite('.claude-plugin/plugin.json', lambda d: d.update(version='0.0.0-invalid'))
        self.assertIn('Claude plugin version differs from VERSION', validator.distribution_errors(self.root))

    def test_marketplace_cannot_omit_shared_resources(self):
        self.rewrite('.claude-plugin/marketplace.json', lambda d: d['plugins'][0].update(source='./skills/cyber-audit'))
        self.assertIn('Claude marketplace must include the whole library root', validator.distribution_errors(self.root))

    def test_mitre_reuse_and_commit_must_match_provenance(self):
        relative = 'skills/cyber-audit/references/repositories.json'
        original = (self.root/relative).read_text()
        for update in ({'reuse_kind':'reference-only'}, {'commit':'wrong'}, {'provenance':'missing.json'}):
            with self.subTest(update=update):
                (self.root/relative).write_text(original)
                self.rewrite(relative, lambda d: next(r for r in d['repositories']
                             if r['repository']=='mitre-attack/attack-stix-data').update(update))
                self.assertIn('MITRE repository reuse differs from bundled provenance', validator.distribution_errors(self.root))

    def test_relocated_release_preserves_plugin_and_runs_from_target(self):
        result = packager.package(out_dir=Path(self.temp.name)/'release')
        relocated = Path(self.temp.name)/'relocated'
        with zipfile.ZipFile(result['archive']) as archive:
            self.assertIn(packager.PREFIX+'.claude-plugin/plugin.json', archive.namelist())
            self.assertIn(packager.PREFIX+'.claude-plugin/marketplace.json', archive.namelist())
            archive.extractall(relocated)
        library = (relocated/'prysmial-sentinel').resolve()
        self.assertEqual(validator.validate(library)['errors'], [])
        expected = {p.parent.name for p in (ROOT/'skills').glob('*/SKILL.md')}
        actual = {p.parent.name for p in (library/'skills').glob('*/SKILL.md')}
        self.assertTrue(actual)
        self.assertEqual(actual, expected)
        target = Path(self.temp.name)/'project'
        target.mkdir()
        (target/'package.json').write_text(json.dumps({'dependencies':{'express':'5.0.0'}}))
        output = Path(self.temp.name)/'plan.json'
        subprocess.run([sys.executable, '-I', str(library/'skills/cyber-audit/scripts/audit.py'),
                        'plan', str(target), '--out', str(output)], cwd=target, check=True,
                       capture_output=True, text=True, timeout=20)
        plan = json.loads(output.read_text())
        self.assertEqual(plan['kind'], 'audit-plan')
        self.assertTrue(plan['modules'])
        for entry in plan['modules']+plan['skills']:
            resource = Path(entry['path'])
            self.assertTrue(resource.is_file())
            self.assertTrue(resource.is_relative_to(library))


if __name__ == '__main__':
    unittest.main()

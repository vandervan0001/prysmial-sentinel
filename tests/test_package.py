import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
import warnings
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('package_library', ROOT/'scripts/package_library.py')
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()/'source'
        self.root.mkdir()
        for name,text in [('README.md','Fixture'),('CITATION.cff','cff-version: 1.2.0'),('.gitignore','output/'),('VERSION','1.2.3')]:
            (self.root/name).write_text(text)
        (self.root/'scripts').mkdir()
        (self.root/'scripts/tool.py').write_text('print("synthetic")\n')

    def build(self):
        return package.package(root=self.root)

    def alter(self, transform):
        result=self.build()
        with zipfile.ZipFile(result['archive']) as z:
            entries={n:z.read(n) for n in z.namelist()}
        transform(entries)
        target=Path(self.temp.name)/'altered.zip'
        with zipfile.ZipFile(target,'w') as z:
            for name,data in entries.items(): z.writestr(name,data)
        return target

    def test_package_is_repeatable_despite_source_timestamps(self):
        first=self.build()
        os.utime(self.root/'README.md',(1700000000,1700000000))
        second=package.package(root=self.root,out_dir=Path(self.temp.name)/'second')
        self.assertEqual(first['sha256'],second['sha256'])
        self.assertGreater(first['files'],0)
        self.assertEqual(package.verify_archive(first['archive'],first['sha256'])['files'],first['files'])

    def test_existing_release_is_not_replaced(self):
        result=self.build()
        before=Path(result['archive']).read_bytes()
        with self.assertRaises(FileExistsError): self.build()
        self.assertEqual(Path(result['archive']).read_bytes(),before)

    def test_tampered_member_is_rejected(self):
        target=self.alter(lambda entries: entries.update({package.PREFIX+'README.md':b'changed'}))
        with self.assertRaisesRegex(ValueError,'checksum mismatch'): package.verify_archive(target)

    def test_unlisted_member_is_rejected(self):
        target=self.alter(lambda entries: entries.update({package.PREFIX+'unexpected':b'data'}))
        with self.assertRaisesRegex(ValueError,'differ from the manifest'): package.verify_archive(target)

    def test_traversal_member_is_rejected_without_extraction(self):
        target=self.alter(lambda entries: entries.update({package.PREFIX+'../escaped':b'data'}))
        with self.assertRaisesRegex(ValueError,'Unsafe'): package.verify_archive(target)
        self.assertFalse((Path(self.temp.name)/'escaped').exists())

    def test_duplicate_archive_member_is_rejected(self):
        result=self.build()
        with warnings.catch_warnings():
            warnings.simplefilter('ignore',UserWarning)
            with zipfile.ZipFile(result['archive'],'a') as z:
                z.writestr(package.PREFIX+'README.md','duplicate')
        with self.assertRaisesRegex(ValueError,'Duplicate'): package.verify_archive(result['archive'])

    def test_wrong_expected_digest_is_rejected(self):
        result=self.build()
        with self.assertRaisesRegex(ValueError,'expected value'): package.verify_archive(result['archive'],'0'*64)

    def test_linked_source_is_rejected(self):
        (self.root/'scripts/linked.py').symlink_to(self.root/'scripts/tool.py')
        with self.assertRaisesRegex(ValueError,'symbolic link'): self.build()

    def test_private_outputs_are_excluded(self):
        (self.root/'output').mkdir()
        (self.root/'output/private.json').write_text('SYNTHETIC_PRIVATE')
        result=self.build()
        with zipfile.ZipFile(result['archive']) as z:
            self.assertNotIn(package.PREFIX+'output/private.json',z.namelist())
            self.assertIn(package.PREFIX+'scripts/tool.py',z.namelist())


if __name__ == '__main__':
    unittest.main()

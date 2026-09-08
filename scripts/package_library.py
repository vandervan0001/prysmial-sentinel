#!/usr/bin/env python3
"""Build repeatable release ZIPs and verify their complete file manifests without extraction."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'prysmial-sentinel/'
MANIFEST = PREFIX+'FILE_SHA256.json'
FILE_LIMIT = 32*1024*1024
TOTAL_LIMIT = 128*1024*1024


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def safe_name(name):
    path = PurePosixPath(name)
    return (bool(name) and not path.is_absolute() and chr(92) not in name
            and ':' not in name and all(p not in {'', '.', '..'} for p in name.split('/')))


def verify_archive(archive, expected_sha256=None):
    path = Path(archive)
    if path.stat().st_size > TOTAL_LIMIT:
        raise ValueError('Archive exceeds size limit')
    actual = sha256(path.read_bytes())
    if expected_sha256 is not None and actual != expected_sha256:
        raise ValueError('Archive checksum differs from the expected value')
    with zipfile.ZipFile(path) as z:
        entries = z.infolist()
        names = [i.filename for i in entries]
        if len(names) != len(set(names)):
            raise ValueError('Duplicate archive members')
        if any(not safe_name(n) or not n.startswith(PREFIX) for n in names):
            raise ValueError('Unsafe or unexpected archive path')
        if any(i.file_size > FILE_LIMIT or stat.S_ISLNK(i.external_attr >> 16) for i in entries):
            raise ValueError('Oversized file or symbolic link in archive')
        if sum(i.file_size for i in entries) > TOTAL_LIMIT:
            raise ValueError('Expanded archive exceeds size limit')
        if MANIFEST not in names or z.getinfo(MANIFEST).file_size > 2*1024*1024:
            raise ValueError('Missing or oversized file manifest')
        manifest = json.loads(z.read(MANIFEST))
        if not isinstance(manifest, dict) or not manifest:
            raise ValueError('Nonempty file manifest required')
        for name, expected in manifest.items():
            if not safe_name(name) or not isinstance(expected,str) or not re.fullmatch(r'[0-9a-f]{64}',expected):
                raise ValueError('Invalid file manifest entry')
        if set(names) != {PREFIX+n for n in manifest} | {MANIFEST}:
            raise ValueError('Archive files differ from the manifest')
        for name, expected in manifest.items():
            if sha256(z.read(PREFIX+name)) != expected:
                raise ValueError('Archive file checksum mismatch: '+name)
    return {'archive':str(path),'files':len(manifest),'bytes':path.stat().st_size,'sha256':actual,
            'note':'Integrity checked. Authenticity depends on obtaining the expected digest from a trusted channel.'}


def package(version=None, out_dir=None, root=ROOT):
    root = Path(root).resolve()
    version = version or (root/'VERSION').read_text().strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+(?:-[A-Za-z0-9.-]+)?',version):
        raise ValueError('A semantic release version is required')
    selected = []
    for directory in ('skills','scripts','tests','examples','.github'):
        base = root/directory
        if base.is_symlink():
            raise ValueError('Package source directory is a symbolic link')
        for p in base.rglob('*'):
            if p.is_symlink():
                raise ValueError('Package source contains a symbolic link')
            if not p.is_file(): continue
            if '__pycache__' in p.parts or p.name.startswith('._') or p.name == '.DS_Store' or p.suffix == '.pyc': continue
            selected.append(p)
    selected += list(root.glob('*.md'))+[root/'.gitignore',root/'CITATION.cff',root/'VERSION']
    contents = {}
    total = 0
    for p in sorted(set(selected)):
        if p.is_symlink() or not p.is_file() or p.resolve() != p:
            raise ValueError('Package source is not a regular local path')
        if p.stat().st_size > FILE_LIMIT:
            raise ValueError('Package source file exceeds size limit')
        data = p.read_bytes()
        total += len(data)
        if len(data) > FILE_LIMIT or total > TOTAL_LIMIT:
            raise ValueError('Package source exceeds size limits')
        contents[p.relative_to(root).as_posix()] = data
    manifest = {name:sha256(data) for name,data in contents.items()}
    out = Path(out_dir) if out_dir is not None else root/'dist'
    out.mkdir(parents=True,exist_ok=True)
    target = out/('prysmial-sentinel-'+version+'.zip')
    contents['FILE_SHA256.json'] = (json.dumps(manifest,indent=2,sort_keys=True)+'\n').encode()
    # Exclusive creation; fixed timestamps and modes make identical input bytes repeatable.
    with target.open('xb') as stream, zipfile.ZipFile(stream,'w',zipfile.ZIP_DEFLATED) as z:
        for name,data in sorted(contents.items()):
            entry = zipfile.ZipInfo(PREFIX+name,date_time=(1980,1,1,0,0,0))
            entry.create_system = 3
            entry.external_attr = (stat.S_IFREG | 0o644) << 16
            entry.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(entry,data,compresslevel=9)
    result = verify_archive(target)
    with (out/(target.name+'.sha256')).open('x') as stream:
        stream.write(result['sha256']+'  '+target.name+'\n')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command',required=True)
    build = sub.add_parser('build')
    build.add_argument('--version')
    build.add_argument('--out-dir',type=Path)
    verify = sub.add_parser('verify')
    verify.add_argument('archive',type=Path)
    verify.add_argument('--sha256')
    args = parser.parse_args()
    try:
        result = package(args.version,args.out_dir) if args.command == 'build' else verify_archive(args.archive,args.sha256)
    except (OSError,ValueError,KeyError,zipfile.BadZipFile) as exc:
        parser.exit(2,'Package check failed: '+str(exc)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()

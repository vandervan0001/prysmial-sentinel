#!/usr/bin/env python3
"""Create a verified distributable archive, excluding Git, private audit outputs and caches."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]


def package():
    selected=[]
    for root in ('skills','scripts','tests'):
        for p in (ROOT/root).rglob('*'):
            if not p.is_file() or p.is_symlink(): continue
            if '__pycache__' in p.parts or p.name.startswith('._') or p.name=='.DS_Store' or p.suffix=='.pyc': continue
            selected.append(p)
    selected += list(ROOT.glob('*.md'))+[ROOT/'.gitignore',ROOT/'CITATION.cff']
    selected=sorted(set(selected))
    manifest={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in selected}
    out=ROOT/'dist'
    out.mkdir(exist_ok=True)
    target=out/'prysmial-sentinel-2026-09-08.zip'
    if target.exists(): raise FileExistsError('Archive exists; choose or preserve prior release explicitly.')
    with zipfile.ZipFile(target,'x',zipfile.ZIP_DEFLATED) as z:
        for p in selected: z.write(p,'prysmial-sentinel/'+p.relative_to(ROOT).as_posix())
        z.writestr('prysmial-sentinel/FILE_SHA256.json',json.dumps(manifest,indent=2)+'\n')
    with zipfile.ZipFile(target) as z:
        bad=z.testzip()
        if bad: raise ValueError('Corrupt ZIP entry '+bad)
        for name,expected in manifest.items():
            if hashlib.sha256(z.read('prysmial-sentinel/'+name)).hexdigest()!=expected:
                raise ValueError('Archive content mismatch: '+name)
    sha=hashlib.sha256(target.read_bytes()).hexdigest()
    (out/(target.name+'.sha256')).write_text(sha+'  '+target.name+'\n')
    return {'archive':str(target),'files':len(manifest),'bytes':target.stat().st_size,'sha256':sha}


if __name__=='__main__': print(json.dumps(package(),indent=2))

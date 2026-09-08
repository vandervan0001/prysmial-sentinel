#!/usr/bin/env python3
"""Register this collection through non-overwriting symlinks. Dry-run by default."""
import argparse
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def install(destination, apply=False):
    dest = Path(destination).expanduser().absolute()
    skills = sorted(p for p in (ROOT/'skills').glob('cyber-*') if (p/'SKILL.md').is_file())
    plan = []
    for src in skills:
        target = dest/src.name
        exists = os.path.lexists(target)
        same = target.is_symlink() and target.resolve() == src.resolve()
        status = 'already-linked' if same else ('collision' if exists else 'create-link')
        plan.append({'name':src.name,'source':str(src),'destination':str(target),'status':status})
    if any(item['status'] == 'collision' for item in plan):
        return {'status':'blocked-by-collision','applied':False,'skills':plan}
    if apply:
        dest.mkdir(parents=True,exist_ok=True)
        for item in plan:
            if item['status'] == 'create-link':
                # Exclusive OS operation; concurrent additions are never replaced.
                Path(item['destination']).symlink_to(item['source'],target_is_directory=True)
    return {'status':'installed' if apply else 'preview','applied':apply,'skills':plan}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    codex_dir = Path(os.environ.get('CODEX_HOME',str(Path.home()/'.codex')))
    parser.add_argument('--dest',default=str(codex_dir/'skills'))
    parser.add_argument('--apply',action='store_true')
    args = parser.parse_args()
    try:
        result = install(args.dest,args.apply)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 2 if result['status'] == 'blocked-by-collision' else 0
    except OSError as exc:
        print(json.dumps({'status':'failed','error':str(exc),'note':'Existing skills were not overwritten; rerun preview to inspect any links already created.'}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())

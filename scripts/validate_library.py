#!/usr/bin/env python3
"""Validate original skill links, catalog consistency, metadata and vendored file integrity."""
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def distribution_errors(root):
    errors = []
    plugin = json.loads((root/'.claude-plugin/plugin.json').read_text())
    marketplace = json.loads((root/'.claude-plugin/marketplace.json').read_text())
    if plugin.get('version') != (root/'VERSION').read_text().strip():
        errors.append('Claude plugin version differs from VERSION')
    entries = marketplace.get('plugins', [])
    if len(entries) != 1 or entries[0].get('name') != plugin.get('name'):
        errors.append('Claude marketplace does not select this plugin')
    elif entries[0].get('source') != './':
        errors.append('Claude marketplace must include the whole library root')
    registry = json.loads((root/'skills/cyber-audit/references/repositories.json').read_text())['repositories']
    if len({r['repository'] for r in registry}) != len(registry):
        errors.append('Duplicate repository entries')
    mitre = [r for r in registry if r['repository'] == 'mitre-attack/attack-stix-data']
    provenance_path = 'skills/cyber-core/references/attack/provenance.json'
    provenance = json.loads((root/provenance_path).read_text())
    if (len(mitre) != 1 or mitre[0].get('reuse_kind') != 'derived-data'
            or mitre[0].get('provenance') != provenance_path
            or mitre[0].get('commit') != provenance['commit']):
        errors.append('MITRE repository reuse differs from bundled provenance')
    return errors


def validate(root=ROOT):
    errors = distribution_errors(root)
    base = root/'skills'
    skills = sorted(base.glob('cyber-*'))
    data = json.loads((base/'cyber-audit/references/catalog.json').read_text())
    catalog = data['skills']
    names = [item['name'] for item in catalog]
    actual = [p.name for p in skills]
    if len(names) != len(set(names)): errors.append('Duplicate catalogue entry')
    if set(actual) != set(names)|{'cyber-audit'}: errors.append('Catalogue and skill directories differ')
    source_records = json.loads((base/'cyber-audit/references/sources.json').read_text())['sources']
    sources = {s['id'] for s in source_records}
    if len(sources) != len(source_records): errors.append('Duplicate source IDs')
    modules_by_name = {m['name']:m for m in data['modules']}
    if len(modules_by_name) != len(data['modules']): errors.append('Duplicate module IDs')
    for domain in catalog:
        declared = domain['modules']
        expected = {m['name'] for m in data['modules'] if m['domain']==domain['name']}
        if len(set(declared)) != len(declared) or set(declared) != expected:
            errors.append('Domain module ownership mismatch: '+domain['name'])
    for entry in data['modules']:
        if set(entry['sources'])-sources: errors.append('Unknown source in '+entry['name'])
        if entry['domain'] not in names: errors.append('Unknown domain in '+entry['name'])
        if not (base/entry['path']).is_file(): errors.append('Missing module '+entry['name'])
        if entry['module'] != Path(entry['path']).stem or entry['name'] != 'cyber-'+entry['module']:
            errors.append('Module identity mismatch: '+entry['name'])
    checked_links = 0
    for skill in skills:
        path = skill/'SKILL.md'
        text = path.read_text()
        match = re.match(r'---\n(.*?)\n---\n',text,re.S)
        if not match:
            errors.append(str(path)+': missing frontmatter')
            continue
        fields = {}
        for line in match.group(1).splitlines():
            key,sep,value = line.partition(':')
            if not sep: errors.append(str(path)+': malformed frontmatter')
            fields[key] = value.strip()
        if fields.get('name') != skill.name: errors.append(str(path)+': name mismatch')
        if not fields.get('description'): errors.append(str(path)+': description missing')
        if len(text.splitlines()) > 180: errors.append(str(path)+': entrypoint too large')
        ui = (skill/'agents/openai.yaml').read_text()
        if '$'+skill.name not in ui: errors.append(str(skill)+': prompt lacks invocation')
        short = re.search(r'short_description: (.*)',ui)
        if not short or not 25 <= len(json.loads(short.group(1))) <= 64:
            errors.append(str(skill)+': invalid UI short description')
        for md in skill.rglob('*.md'):
            if 'upstream' in md.parts: continue
            for label,target in re.findall(r'\[([^\]]*)\]\(([^)]+)\)',md.read_text()):
                if target.startswith(('https://','http://','#','mailto:')): continue
                local = target.split('#',1)[0]
                if not (md.parent/local).exists(): errors.append(str(md)+': broken link '+target)
                checked_links += 1
    lock = json.loads((base/'cyber-audit/references/upstream-lock.json').read_text())
    upstream = base/'cyber-audit/references/upstream/trailofbits'
    for name,expected in lock['files'].items():
        path = upstream/name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            errors.append('Upstream integrity mismatch: '+name)
    actual_vendor = {p.relative_to(upstream).as_posix() for p in upstream.rglob('*') if p.is_file()}
    if actual_vendor != set(lock['files']): errors.append('Untracked files in upstream snapshot')
    attack=base/'cyber-core/references/attack'
    provenance=json.loads((attack/'provenance.json').read_text())
    if hashlib.sha256((attack/'index.json').read_bytes()).hexdigest() != provenance['index_sha256']:
        errors.append('MITRE index integrity mismatch')
    controls=json.loads((base/'cyber-core/references/controls.json').read_text())['controls']
    if len({c['id'] for c in controls})!=len(controls): errors.append('Duplicate control IDs')
    for record in controls:
        for ref in record.get('references',[]):
            parsed = urlsplit(ref)
            if ref not in sources and not (parsed.scheme == 'https' and parsed.netloc):
                errors.append('Unknown control source: '+record['id'])
        if record.get('domain') not in names: errors.append('Unknown control domain: '+record['id'])
        if 'source_path' in record:
            path=root/record['source_path']
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=record['source_sha256']:
                errors.append('Stale compiled control: '+record['id'])
    for md in list(root.glob('*.md'))+list((root/'examples').glob('*.md')):
        for _,target in re.findall(r'\[([^\]]*)\]\(([^)]+)\)',md.read_text()):
            if target.startswith(('https://','http://','#','mailto:')): continue
            if not (md.parent/target.split('#',1)[0]).exists(): errors.append(str(md)+': broken link '+target)
            checked_links+=1
    repositories = json.loads((base/'cyber-audit/references/repositories.json').read_text())['repositories']
    return {'skills':len(skills),'modules':len(data['modules']),'source_references':len(sources),'repository_references':len(repositories),'local_links':checked_links,
            'controls':len(controls),'upstream_files':len(lock['files']),'errors':errors}


if __name__ == '__main__':
    result = validate()
    print(json.dumps(result,indent=2,ensure_ascii=False))
    raise SystemExit(bool(result['errors']))

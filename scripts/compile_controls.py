#!/usr/bin/env python3
"""Compile authored module procedures and domain controls into the canonical query index."""
from pathlib import Path
import hashlib
import json
import re

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'skills/cyber-core/references'


def compile_records():
    catalog=json.loads((ROOT/'skills/cyber-audit/references/catalog.json').read_text())
    records=[]
    for module in catalog['modules']:
        source=ROOT/'skills'/module['path']
        text=source.read_text()
        section=text.split('## Procedure\n\n',1)[1].split('\n## Required evidence',1)[0]
        steps=[m.group(1).strip() for m in re.finditer(r'^\d+\. (.*?)(?=\n\n\d+\.|\Z)',section,re.S|re.M)]
        proof=text.split('## Required evidence\n\n',1)[1].split('\n## ',1)[0].strip()
        tool_note=text.split('## Tools and limits\n\n',1)[1].split('\n## ',1)[0].strip()
        records.append({'id':module['domain'][6:].upper()+'-'+module['module'].upper(),
            'domain':module['domain'],'title':module['title'],
            'applies_to':{'signals':module['tags'],'protocols':[],'vendors':[]},
            'knowledge':{'concepts':[module['title']],'questions':steps},
            'workflow':[{'phase':'review','instruction':s} for s in steps],
            'verification':{'acceptance':proof,'positive_control_required':True},
            'tools':{'passive':[],'active':[],'selection_note':tool_note},
            'safety':{'default_mode':'read-only','active_testing_requires_authorization':True,'production_ot':module['domain']=='cyber-ot'},
            'references':module['sources'],'source_path':str(source.relative_to(ROOT)),
            'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest()})
    extra=json.loads((BASE/'domain-controls.json').read_text())['controls']
    records.extend(extra)
    errors=validate_records(records)
    if errors: raise ValueError('\n'.join(errors))
    return {'schema_version':1,'kind':'cyber-control-catalog','authored_baseline':'2026-09-08','controls':records,
            'note':'Generated from module procedures and domain-controls.json. No tool execution or automatic permission grant.'}


def validate_records(records):
    errors=[]
    seen=set()
    required={'id','domain','title','applies_to','knowledge','workflow','verification','tools','safety','references'}
    for r in records:
        rid=r.get('id','unnamed')
        if required-r.keys(): errors.append(rid+': required fields missing')
        if rid in seen: errors.append(rid+': duplicate id')
        seen.add(rid)
        if not re.fullmatch(r'[A-Z][A-Z0-9-]+',rid): errors.append(rid+': invalid id')
        if not r.get('workflow'): errors.append(rid+': empty procedure')
        if not r.get('verification',{}).get('acceptance'): errors.append(rid+': no acceptance criterion')
        if not r.get('references'): errors.append(rid+': no provenance')
        if r.get('safety',{}).get('active_testing_requires_authorization') is not True: errors.append(rid+': active-test scope boundary missing')
        if r.get('safety',{}).get('default_mode') != 'read-only': errors.append(rid+': default operation must remain read-only')
        if r.get('domain')=='cyber-ot' and r.get('safety',{}).get('production_ot') is not True: errors.append(rid+': OT boundary missing')
        for step in r.get('workflow',[]):
            if not step.get('instruction'): errors.append(rid+': empty step')
    return errors


if __name__=='__main__':
    data=compile_records()
    (BASE/'controls.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'controls':len(data['controls']),'output':str(BASE/'controls.json')}))

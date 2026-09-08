#!/usr/bin/env python3
"""Build a new ATT&CK index from explicitly supplied local bundles; no network or replacement."""
import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
import re

TYPES={'attack-pattern','course-of-action','relationship','x-mitre-tactic','x-mitre-data-source',
       'x-mitre-data-component','x-mitre-detection-strategy','x-mitre-analytic'}
DOMAINS={'enterprise-attack','ics-attack','mobile-attack'}


def transform(bundle,domain):
    if domain not in DOMAINS: raise ValueError('unknown ATT&CK domain')
    if bundle.get('type')!='bundle' or not isinstance(bundle.get('objects'),list):
        raise ValueError('STIX bundle with objects required')
    result=[]
    for obj in bundle['objects']:
        if obj.get('revoked') or obj.get('x_mitre_deprecated') or obj.get('type') not in TYPES: continue
        if not isinstance(obj.get('id'),str): raise ValueError('STIX object ID missing')
        ext=next((e for e in obj.get('external_references',[]) if e.get('source_name') in ('mitre-attack','mitre-ics-attack','mitre-mobile-attack')), {})
        item={'stix_id':obj['id'],'type':obj['type'],'domain':domain,'name':obj.get('name'),
              'attack_id':ext.get('external_id'),'url':ext.get('url'),'modified':obj.get('modified'),
              'description':obj.get('description','')}
        for key in ('source_ref','target_ref','relationship_type','kill_chain_phases','x_mitre_platforms','x_mitre_is_subtechnique'):
            if key in obj: item[key]=obj[key]
        result.append(item)
    if not any(x['type']=='attack-pattern' for x in result): raise ValueError('No active technique: import incomplete')
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--bundle',action='append',required=True,help='domain=/absolute/path/to/bundle.json')
    p.add_argument('--commit',required=True)
    p.add_argument('--license',required=True)
    p.add_argument('--out-dir',required=True)
    args=p.parse_args()
    if not re.fullmatch(r'[0-9a-f]{40}',args.commit): p.error('full source commit required')
    inputs=[]; objects=[]; seen=set()
    for arg in args.bundle:
        domain,sep,path=arg.partition('=')
        if not sep or domain in seen: p.error('unique domain=path arguments required')
        seen.add(domain)
        raw=Path(path).read_bytes()
        if len(raw)>100*1024*1024: p.error('bundle exceeds 100 MiB')
        bundle=json.loads(raw)
        objects.extend(transform(bundle,domain))
        inputs.append({'domain':domain,'url':'https://raw.githubusercontent.com/mitre-attack/attack-stix-data/'+args.commit+'/'+domain+'/'+domain+'.json',
                       'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'objects_raw':len(bundle['objects'])})
    license_data=Path(args.license).read_bytes()
    if b'MITRE' not in license_data: p.error('MITRE license attribution required')
    out=Path(args.out_dir)
    out.mkdir(parents=True,exist_ok=False)
    index=json.dumps({'source_repository':'mitre-attack/attack-stix-data','commit':args.commit,'objects':objects},ensure_ascii=False,separators=(',',':'))+'\n'
    (out/'index.json').write_text(index)
    (out/'LICENSE.txt').write_bytes(license_data)
    provenance={'retrieved_at':None,'compiled_at':dt.datetime.now(dt.timezone.utc).isoformat(),'commit':args.commit,
                'license_file':'LICENSE.txt','transformation':'Active technique, mitigation, tactic, detection and relationship objects. Revoked/deprecated objects excluded. Selected fields only; not a full STIX bundle.',
                'inputs':inputs,'index_sha256':hashlib.sha256(index.encode()).hexdigest(),
                'note':'Local bundle content must be compared to the declared remote commit before accepting this candidate index.'}
    (out/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    print(json.dumps({'objects':len(objects),'out_dir':str(out),'domains':sorted(seen)}))


if __name__=='__main__': main()

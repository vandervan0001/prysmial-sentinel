#!/usr/bin/env python3
"""Check assessment evidence references and status requirements; never certify their truth."""
import argparse
import collections
import json
from pathlib import Path
import re


def validate(data):
    errors = []
    if not isinstance(data, dict):
        return {'valid': False, 'errors': ['Assessment must be an object']}

    def error(where, message):
        errors.append(where+': '+message)

    def text(record, key, where):
        value = record.get(key)
        if not isinstance(value, str) or not value.strip():
            error(where, key+' must be nonempty text')

    def records(key):
        value = data.get(key)
        if not isinstance(value, list):
            error(key, 'must be an array')
            return []
        result = []
        seen = set()
        for i, record in enumerate(value):
            where = key+'['+str(i)+']'
            if not isinstance(record, dict):
                error(where, 'must be an object')
                continue
            rid = record.get('id')
            if not isinstance(rid, str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,127}', rid):
                error(where, 'invalid id')
            elif rid in seen:
                error(where, 'duplicate id')
            else:
                seen.add(rid)
            result.append((where, record))
        return result

    def references(record, key, known, where, required=False):
        value = record.get(key, [])
        if not isinstance(value, list) or any(not isinstance(v, str) for v in value):
            error(where, key+' must be an array of IDs')
            return
        if required and not value:
            error(where, key+' must identify supporting records')
        if any(v not in known for v in value):
            error(where, key+' contains unknown IDs')

    def execution(record, key, where):
        value = record.get(key)
        if not isinstance(value, dict):
            error(where, key+' must record execution')
            return
        n = value.get('cases_run')
        if not isinstance(n, int) or isinstance(n, bool) or n < 1:
            error(where, key+'.cases_run must be positive')
        for field in ('method', 'positive_control', 'expected', 'observed'):
            text(value, field, where+'.'+key)

    if type(data.get('schema_version')) is not int or data.get('schema_version') != 1 or data.get('kind') != 'security-assessment':
        error('assessment', 'schema_version 1 and kind security-assessment required')
    target = data.get('target')
    if not isinstance(target, dict):
        error('target', 'must be an object')
    else:
        for key in ('name', 'revision', 'environment', 'scope'):
            text(target, key, 'target')
    if not isinstance(data.get('limitations'), list) or any(
        not isinstance(v, str) or not v.strip() for v in data.get('limitations', [])
    ):
        error('limitations', 'must be an array of nonempty strings')

    evidence = records('evidence')
    controls = records('controls')
    findings = records('findings')
    evidence_ids = {r['id'] for _, r in evidence if isinstance(r.get('id'), str)}
    control_ids = {r['id'] for _, r in controls if isinstance(r.get('id'), str)}
    for where, record in evidence:
        for key in ('kind', 'source', 'observation'):
            text(record, key, where)
        if not isinstance(record.get('sha256'), str) or not re.fullmatch(r'[0-9a-f]{64}', record['sha256']):
            error(where, 'sha256 must identify the collected evidence bytes')
    if not controls:
        error('controls', 'at least one scoped control is required')
    counts = collections.Counter()
    for where, record in controls:
        status = record.get('status')
        if not isinstance(status, str) or status not in {'tested', 'partial', 'not-tested', 'not-applicable', 'blocked'}:
            error(where, 'unknown control status')
            continue
        counts[status] += 1
        for key in ('asset', 'method'):
            text(record, key, where)
        references(record, 'evidence', evidence_ids, where, status in {'tested', 'partial'})
        if status == 'tested':
            execution(record, 'execution', where)
            if record.get('outcome') not in ('pass', 'fail', 'mixed'):
                error(where, 'tested control needs an outcome separate from coverage')
        else:
            text(record, 'reason', where)
    for where, record in findings:
        status = record.get('status')
        if not isinstance(status, str) or status not in {'candidate', 'confirmed', 'rejected', 'needs-context', 'fixed', 'retested'}:
            error(where, 'unknown finding status')
            continue
        text(record, 'title', where)
        references(record, 'controls', control_ids, where, True)
        references(record, 'evidence', evidence_ids, where, status in {'confirmed', 'fixed', 'retested', 'rejected'})
        if status in {'confirmed', 'fixed', 'retested'}:
            for key in ('mechanism', 'preconditions', 'impact', 'attempt_to_disprove', 'remediation'):
                text(record, key, where)
        if status in {'rejected', 'needs-context'}:
            text(record, 'reason', where)
        if status in {'fixed', 'retested'}:
            text(record, 'fix_revision', where)
        if status == 'retested':
            execution(record, 'retest', where)
            retest = record.get('retest')
            if not isinstance(retest, dict) or retest.get('outcome') != 'pass':
                error(where, 'a failed retest leaves the defect confirmed or needs-context')
            references(record, 'retest_evidence', evidence_ids, where, True)
    return {'valid': not errors, 'errors': errors, 'controls': len(controls),
            'coverage_counts': dict(counts), 'findings': len(findings),
            'note': 'Structural evidence checks only. Evidence truth, authorization and security require review.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    args = parser.parse_args()
    try:
        with args.input.open('rb') as stream:
            raw = stream.read(32*1024*1024+1)
        if len(raw) > 32*1024*1024:
            raise ValueError('Assessment exceeds the 32 MiB input limit')
        result = validate(json.loads(raw))
    except (OSError, ValueError, TypeError):
        result = {'valid': False, 'errors': ['Could not read a valid bounded assessment JSON file']}
    print(json.dumps(result, indent=2))
    return 0 if result['valid'] else 2


if __name__ == '__main__':
    raise SystemExit(main())

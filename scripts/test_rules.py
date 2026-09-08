#!/usr/bin/env python3
"""Exercise the real scanner and compare every ruleid/ok fixture annotation."""
import importlib.util
import json
from pathlib import Path
import re
import tempfile

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('audit',ROOT/'skills/cyber-audit/scripts/audit.py')
audit=importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


def main():
    source=ROOT/'tests/fixtures/semgrep'
    expected=set()
    safe=set()
    for path in source.iterdir():
        for line,text in enumerate(path.read_text().splitlines(),1):
            match=re.search(r'(ruleid|ok):\s+(cyber-[\w-]+)',text)
            if match:
                (expected if match[1]=='ruleid' else safe).add((path.name,line+1,match[2]))
    if not expected or not safe: raise AssertionError('Non-empty positive and negative fixtures required')
    with tempfile.TemporaryDirectory(prefix='cyber-rules-') as tmp:
        result=audit.scan_local(source,Path(tmp)/'results',execute=True)
        if result['status']!='complete': raise AssertionError('Scanner did not complete: '+str(result))
        data=json.loads((Path(tmp)/'results/candidates.json').read_text())
        actual={(r['path'],r['line'],r['rule'].rsplit('.',1)[-1]) for r in data['findings']}
        missing=expected-actual
        unexpected=actual-expected
        safe_hits=actual&safe
        if missing or unexpected or safe_hits:
            raise AssertionError(str({'missing':sorted(missing),'unexpected':sorted(unexpected),'safe_hits':sorted(safe_hits)}))
        print(json.dumps({'tool':result['tool_version'],'rules':len({x[2] for x in expected}),
                          'positive_cases':len(expected),'negative_cases':len(safe),
                          'actual_findings':len(actual),'analyzed_files':data['analyzed_targets'],'status':'passed'}))


if __name__=='__main__': main()

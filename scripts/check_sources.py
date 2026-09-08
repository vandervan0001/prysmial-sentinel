#!/usr/bin/env python3
"""Read-only HTTP checks. Never change source content, execute downloads or schedule work."""
import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import sys
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'skills/cyber-audit/scripts'))
from audit import private_write


def check(source):
    result = {'id':source['id'],'url':source['url'],'checked_at':dt.datetime.now(dt.timezone.utc).isoformat()}
    req = urllib.request.Request(source['url'],headers={'User-Agent':'Cybersec-Reference-Check/1.0','Accept':'text/html,application/json,text/plain'})
    try:
        with urllib.request.urlopen(req,timeout=15) as response:
            body = response.read(1024*1024)
            result.update(status='reachable',http_status=response.status,final_url=response.url,
                          sampled_bytes=len(body),sample_sha256=hashlib.sha256(body).hexdigest())
            title = re.search(rb'<title[^>]*>(.*?)</title>',body,re.S|re.I)
            if title:
                result['page_title'] = re.sub(r'\s+',' ',title.group(1).decode('utf-8',errors='replace')).strip()[:200]
    except (urllib.error.URLError,TimeoutError,OSError) as exc:
        result.update(status='not-verified',reason=str(exc)[:200])
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',required=True)
    p.add_argument('--id',action='append',default=[])
    args = p.parse_args()
    data = json.loads((ROOT/'skills/cyber-audit/references/sources.json').read_text())['sources']
    unknown = set(args.id)-{s['id'] for s in data}
    if unknown: p.error('Unknown source IDs: '+', '.join(sorted(unknown)))
    if args.id: data = [s for s in data if s['id'] in args.id]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(check,data))
    report = {'kind':'source-link-check','note':'HTTP reachability only; not a scientific or security validation. No sources updated.','results':results}
    private_write(args.out,json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'checked':len(results),'reachable':sum(r['status']=='reachable' for r in results),'out':args.out}))
    return 2 if any(r['status'] != 'reachable' for r in results) else 0


if __name__ == '__main__':
    raise SystemExit(main())

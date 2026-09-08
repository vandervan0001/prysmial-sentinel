#!/usr/bin/env python3
"""Local audit inventory and evidence transport. Python 3.10+, standard library only."""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import signal
import stat
import subprocess
import sys
import tempfile
import time
from urllib.parse import urlsplit, unquote

BASE = Path(__file__).resolve().parents[1]
SKILLS = BASE.parent
EXCLUDE = {'.git', '.hg', '.svn', 'node_modules', '.venv', 'venv', '__pycache__',
           '.next', '.nuxt', 'dist', 'build', 'target', 'vendor', '.terraform',
           '.cache', 'coverage', 'output'}
EXTENSIONS = {'.py':'python', '.js':'javascript', '.mjs':'javascript', '.cjs':'javascript',
              '.jsx':'javascript', '.ts':'typescript', '.tsx':'typescript', '.go':'go',
              '.rs':'rust', '.c':'c', '.h':'c', '.cpp':'cpp', '.hpp':'cpp', '.cc':'cpp',
              '.java':'java', '.kt':'kotlin', '.swift':'swift', '.cs':'csharp',
              '.php':'php', '.rb':'ruby', '.sol':'solidity', '.sh':'shell'}
CODE_SUFFIXES = set(EXTENSIONS) | {'.json', '.yaml', '.yml', '.toml', '.tf', '.html', '.xml'}
TOOLS = ['semgrep', 'codeql', 'gitleaks', 'osv-scanner', 'trivy', 'syft', 'grype',
         'checkov', 'zizmor', 'actionlint', 'nuclei', 'nmap', 'testssl.sh',
         'prowler', 'kube-bench', 'slither', 'forge', 'yara', 'yara-x', 'suricata']


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def private_write(path, content):
    """Exclusive write: never replace prior evidence or follow a final symlink."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w', encoding='utf-8') as stream:
        stream.write(content)


def output(data, path=None):
    serialized = json.dumps(data, indent=2, ensure_ascii=False) + '\n'
    if path:
        private_write(path, serialized)
    else:
        print(serialized, end='')


def read_regular(path, max_bytes=1024*1024):
    """Reject symlinks, special files, oversized input, and link swaps at open."""
    p = Path(path)
    if p.is_symlink():
        raise ValueError('symlink excluded')
    fd = os.open(p, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0) | getattr(os, 'O_NONBLOCK', 0))
    try:
        st = os.fstat(fd)
        if not stat.S_ISREG(st.st_mode):
            raise ValueError('not a regular file')
        if st.st_size > max_bytes:
            raise ValueError('file exceeds size limit')
        with os.fdopen(fd, 'rb', closefd=False) as stream:
            data = stream.read(max_bytes + 1)
        if len(data) > max_bytes:
            raise ValueError('file grew beyond size limit')
        return data
    finally:
        os.close(fd)


def inventory(project, max_files=20000):
    root = Path(project).expanduser().resolve(strict=True)
    if not root.is_dir():
        raise ValueError('project must be a directory')
    if max_files < 1:
        raise ValueError('max_files must be positive')
    paths, skipped, errors, signals = [], [], [], collections.defaultdict(list)
    counts = collections.Counter()
    truncated = False
    def signal(tag, path):
        if len(signals[tag]) < 12 and path not in signals[tag]:
            signals[tag].append(path)
    def walk_error(exc):
        errors.append({'path':str(exc.filename), 'reason':type(exc).__name__})
    for directory, dirs, files in os.walk(root, followlinks=False, onerror=walk_error):
        base = Path(directory)
        keep = []
        for name in sorted(dirs):
            p = base/name
            if name in EXCLUDE or p.is_symlink() or name.startswith('._'):
                skipped.append(str(p.relative_to(root)))
            else:
                keep.append(name)
        dirs[:] = keep
        for name in sorted(files):
            p = base/name
            rel = p.relative_to(root).as_posix()
            if p.is_symlink() or name.startswith('._') or name == '.DS_Store':
                skipped.append(rel)
                continue
            try:
                if not stat.S_ISREG(p.stat().st_mode):
                    skipped.append(rel)
                    continue
            except OSError as exc:
                errors.append({'path':rel,'reason':type(exc).__name__})
                continue
            if len(paths) >= max_files:
                truncated = True
                break
            paths.append(rel)
            ext = p.suffix.lower()
            if ext in EXTENSIONS:
                counts[EXTENSIONS[ext]] += 1
            lower = rel.lower()
            if name in {'package.json','pnpm-lock.yaml','yarn.lock','package-lock.json'}:
                signal('javascript', rel)
            if ext in {'.html','.jsx','.tsx','.vue','.svelte'} or name.startswith(('next.config.','nuxt.config.')):
                signal('web',rel)
            if ext in {'.c','.cpp','.cc','.h','.hpp','.rs'} or name == 'CMakeLists.txt':
                signal('native',rel)
            if ext == '.sol' or name in {'foundry.toml','hardhat.config.ts','Anchor.toml'}:
                signal('blockchain',rel)
            if name.startswith('Dockerfile') or name in {'docker-compose.yml','compose.yaml','compose.yml'}:
                signal('containers',rel)
            if ext == '.tf' or name in {'Chart.yaml','Pulumi.yaml','serverless.yml','wrangler.toml','wrangler.jsonc'}:
                signal('iac',rel)
                signal('cloud',rel)
            if name in {'Chart.yaml','kustomization.yaml'} or '/k8s/' in '/'+lower:
                signal('kubernetes',rel)
            if lower.startswith('.github/workflows/') or name in {'.gitlab-ci.yml','Jenkinsfile','azure-pipelines.yml'}:
                signal('cicd',rel)
            if name in {'AndroidManifest.xml','Info.plist','pubspec.yaml'} or ext in {'.xcodeproj','.apk','.ipa'}:
                signal('mobile',rel)
            if name == 'tauri.conf.json' or 'electron' in lower:
                signal('desktop',rel)
            if name in {'mcp.json','.mcp.json'}:
                signal('mcp',rel)
                signal('ai',rel)
            if any(x in lower for x in ('openapi','swagger','graphql','protobuf')) or ext == '.proto':
                signal('api',rel)
            if any(x in lower for x in ('websocket','socket.io','redis-stream','kafka')):
                signal('realtime',rel)
            if ext in {'.pcap','.pcapng'}:
                signal('network',rel)
            if name == 'platformio.ini' or lower.endswith(('.ioc','.elf','.hex')):
                signal('firmware',rel)
            if ext in {'.scl','.awl','.lad'} or 'modbus' in lower or 'opcua' in lower:
                signal('ot',rel)
            # Read only selected package manifests; never .env or arbitrary source text.
            if name in {'package.json','pyproject.toml','requirements.txt','go.mod','Cargo.toml'}:
                try:
                    data = read_regular(p, 256*1024).decode('utf-8')
                    if name == 'package.json':
                        pkg = json.loads(data)
                        deps = set()
                        for key in ('dependencies','devDependencies','peerDependencies','optionalDependencies'):
                            value = pkg.get(key,{}) if isinstance(pkg,dict) else {}
                            if isinstance(value,dict): deps.update(value)
                        content = ' '.join(deps).lower()
                    else:
                        content = data.lower()
                    for tag, words in {
                        'web':['next','react','django','flask','fastapi','express','svelte','vue'],
                        'ai':['openai','anthropic','langchain','llama-index','transformers','pydantic-ai'],
                        'mcp':['modelcontextprotocol','fastmcp'],
                        'rag':['chromadb','qdrant','pinecone','weaviate','llama-index'],
                        'desktop':['electron','tauri'],
                        'realtime':['socket.io','websockets','aiokafka'],
                        'payments':['stripe','adyen'],
                        'crypto':['cryptography','ring','rustls','libsodium']}.items():
                        if any(word in content for word in words): signal(tag,rel)
                except (OSError, ValueError, UnicodeError) as exc:
                    errors.append({'path':rel,'reason':type(exc).__name__})
        if truncated:
            break
    return {'schema_version':1, 'kind':'inventory', 'created_at':now(), 'root':str(root),
            'files_seen':len(paths), 'files':paths, 'languages':dict(sorted(counts.items())),
            'signals':dict(signals), 'excluded_paths':skipped, 'errors':errors,
            'status':'partial' if truncated or errors else ('empty' if not paths else 'complete'),
            'truncated':truncated, 'limits':{'max_files':max_files,'manifest_bytes':256*1024},
            'limitations':['Filename and bounded manifest heuristics; not a vulnerability scan.',
                           'No source execution, Git history, deployed state or device inspection.',
                           'Directories excluded by the documented fixed list are outside coverage.']}


def make_plan(inv, profile='deep', extra=()):
    catalog = json.loads((BASE/'references/catalog.json').read_text())
    modules = catalog['modules']
    known = {m['name']:m for m in modules}
    domains = {s['name']:s for s in catalog['skills']}
    expanded = set()
    for name in extra:
        if name in domains:
            expanded.update(domains[name]['modules'])
        elif name in known:
            expanded.add(name)
        else:
            raise ValueError('unknown skill: '+name)
    tags = set(inv['signals'])
    if 'web' in tags: tags |= {'api','privacy'}
    selected = {'cyber-code-review','cyber-dependencies','cyber-secrets','cyber-triage'}
    if profile == 'deep': selected |= {'cyber-threat-model','cyber-sast','cyber-research','cyber-remediation'}
    for m in modules:
        if (set(m['tags'])-{'all','active'}) & tags:
            selected.add(m['name'])
    selected.update(expanded)
    order = [m for m in modules if m['name'] in selected]
    domain_names = {m['domain'] for m in order} | (set(extra) & set(domains))
    return {'schema_version':1,'kind':'audit-plan','created_at':now(),'profile':profile,
            'inventory':inv,'skills':[{'name':d,'path':str(SKILLS/d/'SKILL.md'),'status':'not-tested'} for d in sorted(domain_names)],
            'modules':[{'name':m['name'],'domain':m['domain'],'path':str(SKILLS/m['path']),
                                      'reason':'requested' if m['name'] in expanded else
                                      ('baseline' if 'all' in m['tags'] else 'stack signal'),
                                      'status':'not-tested'} for m in order],
            'unselected_modules':[m['name'] for m in modules if m['name'] not in selected],
            'note':'Heuristic plan only. Confirm runtime, cloud, OT and identity surfaces manually. No tests executed.'}


def safe_label(value):
    """Compact metadata only; messages, snippets, secrets and matches are never imported."""
    s = str(value or '')
    s = re.sub(r'(?i)(bearer\s+)\S+', r'\1[REDACTED]', s)
    s = re.sub(r'(?i)((?:token|password|secret|api[_-]?key)\s*[=:]\s*)\S+', r'\1[REDACTED]', s)
    s = re.sub(r'\b(?:gh[pousr]_[A-Za-z0-9_]{16,}|github_pat_[A-Za-z0-9_]{16,}|sk-[A-Za-z0-9_-]{16,}|AKIA[A-Z0-9]{16})\b','[REDACTED]',s)
    s = re.sub(r'https?://[^\s]+', '[URL OMITTED]', s)
    return ''.join(c for c in s if c.isprintable())[:240]


def location(value):
    s = str(value or '')
    parsed = urlsplit(s)
    if parsed.scheme:
        if parsed.scheme != 'file': return '[remote location omitted]'
        s = unquote(parsed.path)
    s = s.split('?',1)[0].split('#',1)[0]
    return safe_label(s)


def positive_line(value):
    return value if isinstance(value,int) and not isinstance(value,bool) and value > 0 else None


def severity(value):
    s = str(value or '').lower()
    return {'error':'high','warning':'medium','warn':'medium','note':'low','info':'info',
            'informational':'info'}.get(s,s if s in {'critical','high','medium','low','info'} else 'unknown')


def normalize(raw, fmt, source_hash):
    """Admit known structures, preserve partial states, never promote scanner severity to proof."""
    rows, warnings = [], []
    status = 'unknown'
    analyzed = None
    tool = fmt
    def add(rule,path='',line=None,sev='unknown',component=None):
        rule, path = safe_label(rule), location(path)
        line = positive_line(line)
        component = safe_label(component) if component else None
        identity = json.dumps([tool,rule,path,line,component],ensure_ascii=False)
        rows.append({'id':'F-'+digest(identity.encode())[:16], 'status':'candidate',
                     'tool':tool,'rule':rule,'title':'Scanner candidate: '+rule,
                     'path':path,'line':line,'scanner_severity':severity(sev),
                     'component':component, 'evidence_sha256':source_hash,
                     'verification':'not-performed'})
    if fmt == 'semgrep':
        if not isinstance(raw,dict) or not isinstance(raw.get('results'),list):
            raise ValueError('invalid Semgrep JSON: results array required')
        if raw.get('errors'):
            warnings.append('Semgrep reports analysis errors: '+str(len(raw['errors'])))
            status = 'partial'
        scans = raw.get('paths',{}).get('scanned')
        if isinstance(scans,list):
            analyzed = len(scans)
            if status != 'partial': status = 'complete' if analyzed else 'no-targets'
        if raw.get('paths',{}).get('skipped'):
            warnings.append('Semgrep skipped targets; review raw paths.skipped under restricted access.')
            status = 'partial'
        for row in raw['results']:
            if not isinstance(row,dict) or 'check_id' not in row or 'path' not in row:
                raise ValueError('malformed Semgrep result')
            add(row['check_id'],row['path'],row.get('start',{}).get('line'),row.get('extra',{}).get('severity'))
    elif fmt == 'sarif':
        if not isinstance(raw,dict) or raw.get('version') != '2.1.0' or not isinstance(raw.get('runs'),list):
            raise ValueError('SARIF 2.1.0 with runs array required')
        completed = []
        for run in raw['runs']:
            if not isinstance(run,dict): raise ValueError('malformed SARIF run')
            tool = safe_label(run.get('tool',{}).get('driver',{}).get('name','sarif'))
            invocations = run.get('invocations',[])
            completed.extend(v.get('executionSuccessful') for v in invocations)
            if not invocations: completed.append(None)
            if any(n.get('level') in {'error','warning'} for v in invocations
                   for n in v.get('toolExecutionNotifications',[])):
                warnings.append('SARIF contains execution diagnostics; inspect raw notifications.')
            results = run.get('results',[])
            if not isinstance(results,list): raise ValueError('malformed SARIF results')
            driver_rules = run.get('tool',{}).get('driver',{}).get('rules',[])
            for row in results:
                if not isinstance(row,dict): raise ValueError('malformed SARIF result')
                rule = row.get('ruleId')
                index = row.get('ruleIndex')
                if rule is None and isinstance(index,int) and 0 <= index < len(driver_rules):
                    rule = driver_rules[index].get('id')
                if rule is None: rule = 'unidentified-rule'
                locations = row.get('locations') or [{}]
                for loc in locations:
                    physical = loc.get('physicalLocation',{})
                    artifact = physical.get('artifactLocation',{})
                    uri = artifact.get('uri')
                    idx = artifact.get('index')
                    if uri is None and isinstance(idx,int) and 0 <= idx < len(run.get('artifacts',[])):
                        uri = run['artifacts'][idx].get('location',{}).get('uri','')
                    add(rule,uri or '',physical.get('region',{}).get('startLine'),row.get('level','warning'))
        # Successful invocation alone does not establish how much code was analyzed.
        status = 'partial' if False in completed or warnings else 'unknown'
        warnings.append('SARIF execution state preserved; analyzed target count is not established.')
    elif fmt == 'gitleaks':
        if not isinstance(raw,list): raise ValueError('Gitleaks JSON must be an array')
        for row in raw:
            if not isinstance(row,dict) or not {'RuleID','File'} <= row.keys():
                raise ValueError('malformed Gitleaks finding')
            commit = row.get('Commit')
            context = 'commit:'+commit if isinstance(commit,str) and re.fullmatch(r'[0-9a-fA-F]{7,64}',commit) else None
            add(row['RuleID'],row['File'],row.get('StartLine'),'unknown',context)
        warnings.append('Gitleaks JSON alone does not establish exit status or coverage.')
    elif fmt == 'trivy':
        if not isinstance(raw,dict) or raw.get('SchemaVersion') != 2:
            raise ValueError('Trivy SchemaVersion 2 required')
        results = raw.get('Results',[])
        if not isinstance(results,list): raise ValueError('malformed Trivy Results')
        for target in results:
            for row in target.get('Vulnerabilities') or []:
                if 'VulnerabilityID' not in row: raise ValueError('Trivy vulnerability lacks id')
                add(row['VulnerabilityID'],target.get('Target',''),None,row.get('Severity'),
                    str(row.get('PkgName',''))+'@'+str(row.get('InstalledVersion','')))
            for row in target.get('Misconfigurations') or []:
                if 'ID' not in row: raise ValueError('Trivy misconfiguration lacks id')
                if row.get('Status') in {'PASS','EXCEPTION'}: continue
                add(row['ID'],target.get('Target',''),row.get('CauseMetadata',{}).get('StartLine'),row.get('Severity'))
            for row in target.get('Secrets') or []:
                add(row.get('RuleID','secret'),target.get('Target',''),row.get('StartLine'),row.get('Severity'))
        warnings.append('Trivy findings alone do not establish scan completion, DB freshness or reachability.')
    else:
        raise ValueError('unsupported format')
    unique = {}
    for row in rows:
        if row['id'] not in unique:
            unique[row['id']] = {**row,'occurrences':1}
        else:
            unique[row['id']]['occurrences'] += 1
    return {'schema_version':1,'kind':'scanner-candidates','created_at':now(),'format':fmt,
            'input_sha256':source_hash, 'scan_status':status,'analyzed_targets':analyzed,
            'warnings':warnings,'candidate_count':len(unique),'findings':list(unique.values()),
            'limitations':['Raw messages, snippets, matches, secrets and URLs are omitted.',
                           'Metadata labels are filtered, not guaranteed anonymous. Review before sharing.',
                           'No finding is confirmed and no control is certified by this import.']}


def report(data):
    if data.get('kind') != 'scanner-candidates': raise ValueError('normalized candidates required')
    def cell(v):
        s = html.escape(str(v if v is not None else 'not reported')).replace('|','&#124;').replace('\n',' ')
        for character in ('[',']','`','*','_','\\'):
            s = s.replace(character,'&#'+str(ord(character))+';')
        return s
    lines = ['# Scanner findings for review','',
             'Scan status: '+cell(data['scan_status'])+'.',
             'Analyzed targets: '+cell(data.get('analyzed_targets'))+'.',
             'Imported findings remain candidates until their cause and impact are verified.','',
             '| ID | Rule | Location | Scanner severity | Status |', '|---|---|---|---|---|']
    for row in data['findings']:
        place = row['path'] + (':'+str(row['line']) if row['line'] else '')
        lines.append('| '+' | '.join(cell(x) for x in [row['id'],row['rule'],place,row['scanner_severity'],row['status']])+' |')
    lines += ['','## Collection limits',''] + ['- '+cell(x) for x in data['warnings']+data['limitations']]
    lines += ['','## Review required','',
              'For each candidate, record the input path, existing checks, preconditions, impact, attempt to disprove the finding, fix and retest. List untested controls separately.','']
    return '\n'.join(lines)


def run_bounded(args,cwd,env,timeout):
    """Bound the whole scanner process group on POSIX, including engine children."""
    with subprocess.Popen(args,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
                          start_new_session=(os.name=='posix')) as proc:
        try:
            stdout,stderr=proc.communicate(timeout=timeout)
            return stdout,stderr,proc.returncode
        except subprocess.TimeoutExpired:
            if os.name=='posix':
                try: os.killpg(proc.pid,signal.SIGKILL)
                except ProcessLookupError: pass
            else:
                proc.kill()
            stdout,stderr=proc.communicate(timeout=10)
            return stdout,stderr,None


def scan_local(project, out_dir=None, execute=False, timeout=120):
    if not 1 <= timeout <= 3600: raise ValueError('timeout must be between 1 and 3600 seconds')
    inv = inventory(project)
    plan = {'kind':'local-scan-plan','root':inv['root'],'tool':'semgrep',
            'rules':str(BASE/'assets/semgrep-rules.yml'), 'execute':False,
            'note':'Bundled rules, isolated bounded file copy, no project execution or install.',
            'limits':{'file_bytes':1024*1024,'total_bytes':128*1024*1024,'timeout_seconds':timeout},
            'inventory_status':inv['status']}
    if not execute: return plan
    binary = shutil.which('semgrep')
    if not binary: raise ValueError('Semgrep is not installed; no installation attempted')
    if not out_dir: raise ValueError('--out-dir is required with --execute')
    destination = Path(out_dir).expanduser().absolute()
    destination.mkdir(parents=True,exist_ok=False,mode=0o700)
    started = now()
    with tempfile.TemporaryDirectory(prefix='cyber-scan-') as temp:
        tmp = Path(temp)
        snapshot = tmp/'source'
        snapshot.mkdir()
        copied, omissions, hashes = [], [], {}
        total = 0
        source_root = Path(inv['root'])
        for rel in inv['files']:
            p = source_root/rel
            if p.suffix.lower() not in CODE_SUFFIXES: continue
            try:
                # Reject a symlinked parent introduced since inventory.
                if p.resolve().relative_to(source_root).as_posix() != rel:
                    raise ValueError('path changed or escaped project')
                data = read_regular(p)
                if total + len(data) > 128*1024*1024:
                    raise ValueError('snapshot byte limit')
                if b'\0' in data: raise ValueError('binary input excluded')
                target = snapshot/rel
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(data)
                hashes[rel] = digest(data)
                copied.append(rel)
                total += len(data)
            except (OSError,ValueError) as exc:
                omissions.append({'path':rel,'reason':str(exc)[:80]})
        env = {k:os.environ[k] for k in ('PATH','LANG','LC_ALL','SYSTEMROOT') if k in os.environ}
        # Task-scoped child environment; do not inherit user credentials or Semgrep settings.
        env.update({'HOME':str(tmp/'home'),'XDG_CONFIG_HOME':str(tmp/'config'),
                    'SEMGREP_SEND_METRICS':'off','SEMGREP_ENABLE_VERSION_CHECK':'0'})
        (tmp/'home').mkdir()
        args = [binary,'scan','--config',str(BASE/'assets/semgrep-rules.yml'),
                '--json','--metrics=off','--disable-version-check','--no-git-ignore',
                '--no-rewrite-rule-ids',
                '--jobs','2','--timeout','10','.']
        version = subprocess.run([binary,'--version'],env=env,capture_output=True,text=True,timeout=30)
        if version.returncode != 0: raise ValueError('Semgrep version check failed')
        if not copied: raise ValueError('No eligible source files: scan not performed')
        t0 = time.monotonic()
        stdout, stderr, rc = run_bounded(args,snapshot,env,timeout)
        duration = round(time.monotonic()-t0,3)
        private_write(destination/'raw-semgrep.json',stdout.decode('utf-8',errors='replace'))
        private_write(destination/'scanner.stderr.txt',stderr.decode('utf-8',errors='replace'))
        metadata = {'schema_version':1,'kind':'local-scan-run','started_at':started,'finished_at':now(),
                    'duration_seconds':duration,'tool':'semgrep','tool_version':safe_label(version.stdout.strip()),
                    'exit_code':rc,'status':'timeout' if rc is None else ('failed' if rc != 0 else 'unknown'),
                    'source_root':inv['root'],'snapshot_files':len(copied),'snapshot_bytes':total,
                    'files_sha256':hashes,'rules_sha256':digest((BASE/'assets/semgrep-rules.yml').read_bytes()),
                    'raw_sha256':digest(stdout),'omissions':omissions,'excluded_paths':inv['excluded_paths'],
                    'inventory_status':inv['status'],'command':args}
        try:
            normalized = normalize(json.loads(stdout),'semgrep',digest(stdout))
            if rc == 0:
                metadata['status'] = normalized['scan_status']
                if omissions or inv['status'] != 'complete': metadata['status'] = 'partial'
            normalized['scan_status'] = metadata['status']
            normalized['warnings'].append('Only bundled rule language targets in the copied snapshot were analyzed; inspect run.json for exclusions.')
            output(normalized,destination/'candidates.json')
            private_write(destination/'candidates.md',report(normalized))
        except (ValueError,TypeError,KeyError,AttributeError):
            metadata['parse_error'] = 'Scanner output could not be normalized; inspect private raw output.'
            if rc == 0: metadata['status'] = 'failed'
        output(metadata,destination/'run.json')
    return {'kind':'local-scan-summary','status':metadata['status'],'output_dir':str(destination),
            'files_copied':len(copied),'tool_version':metadata['tool_version']}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command',required=True)
    for name in ('inventory','plan'):
        cmd = sub.add_parser(name)
        cmd.add_argument('project')
        cmd.add_argument('--max-files',type=int,default=20000)
        cmd.add_argument('--out')
        if name == 'plan':
            cmd.add_argument('--profile',choices=['quick','deep'],default='deep')
            cmd.add_argument('--add',action='append',default=[])
    sub.add_parser('doctor')
    cmd = sub.add_parser('normalize')
    cmd.add_argument('input')
    cmd.add_argument('--format',required=True,choices=['semgrep','sarif','gitleaks','trivy'])
    cmd.add_argument('--out',required=True)
    cmd = sub.add_parser('report')
    cmd.add_argument('input')
    cmd.add_argument('--out',required=True)
    cmd = sub.add_parser('scan-local')
    cmd.add_argument('project')
    cmd.add_argument('--execute',action='store_true')
    cmd.add_argument('--out-dir')
    cmd.add_argument('--timeout',type=int,default=120)
    args = parser.parse_args(argv)
    try:
        if args.command in {'inventory','plan'}:
            result = inventory(args.project,args.max_files)
            if args.command == 'plan': result = make_plan(result,args.profile,args.add)
            output(result,args.out)
        elif args.command == 'doctor':
            output({'python':sys.version.split()[0],'tools':{name:shutil.which(name) for name in TOOLS},
                    'note':'Executable discovery only. No tool is installed or executed by doctor.'})
        elif args.command == 'normalize':
            raw = read_regular(args.input,32*1024*1024)
            output(normalize(json.loads(raw),args.format,digest(raw)),args.out)
        elif args.command == 'report':
            private_write(args.out,report(json.loads(read_regular(args.input,32*1024*1024))))
        elif args.command == 'scan-local':
            result = scan_local(args.project,args.out_dir,args.execute,args.timeout)
            output(result)
            if args.execute and result['status'] != 'complete': return 2
    except (OSError,ValueError,KeyError,TypeError,AttributeError,subprocess.SubprocessError) as exc:
        print('Audit command failed: '+safe_label(str(exc)),file=sys.stderr)
        return 2
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

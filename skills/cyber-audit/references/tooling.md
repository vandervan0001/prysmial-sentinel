# Local tools and external workflows

Inventory, planning and report consolidation require Python 3.10 or later. `scan-local --execute` also requires Semgrep. `doctor` lists executables it finds without installing or running them.

## Commands

Run from the library directory:

```bash
python3 skills/cyber-audit/scripts/audit.py inventory /path/project --out /private/path/inventory.json
python3 skills/cyber-audit/scripts/audit.py plan /path/project --profile deep --add cyber-cloud --out /private/path/plan.json
python3 skills/cyber-audit/scripts/audit.py scan-local /path/project
python3 skills/cyber-audit/scripts/audit.py scan-local /path/project --execute --out-dir /private/path/new-scan
python3 skills/cyber-audit/scripts/audit.py normalize /path/semgrep.json --format semgrep --out /private/path/candidates.json
python3 skills/cyber-audit/scripts/audit.py normalize /path/codeql.sarif --format sarif --out /private/path/codeql-candidates.json
python3 skills/cyber-audit/scripts/audit.py report /private/path/candidates.json --out /private/path/candidates.md
```

Output paths must be new. Writes refuse to replace existing evidence. Supported imports are Semgrep JSON, SARIF 2.1.0, Gitleaks JSON and Trivy SchemaVersion 2. Unknown variants fail explicitly. Imports make no enrichment requests.

Generated reports contain identifiers, locations and scanner severities. They omit raw messages, code, matched content and secrets. Review metadata before sharing; filenames and component names can also be confidential. Raw scanner JSON and stderr stay in the private output directory.

## Bundled scan coverage

`scan-local` copies eligible files to a temporary directory and runs six local rules. It does not build or execute target code. The rules cover selected Python and JavaScript/TypeScript patterns: request data or user input reaching eval, shell or pickle operations, and disabled TLS verification. Taint sources are deliberately limited. The rules do not cover all variants of these issues or the full AppSec catalogue.

Inventory is limited to 20,000 files and 256 KiB per inspected manifest. Scan copies are limited to 1 MiB per file and 128 MiB in total. Symlinks, special files and these directories are excluded: `.git`, `.hg`, `.svn`, `node_modules`, `.venv`, `venv`, `__pycache__`, `.next`, `.nuxt`, `dist`, `build`, `target`, `vendor`, `.terraform`, `.cache`, `coverage`, `output`. Review excluded dependencies and distributed artifacts separately when the scenario requires them.

Exit code 0 from `scan-local --execute` means the process succeeded and Semgrep reported a nonempty scan without errors for the selected scope. Findings may still exist. Exit code 2 means incomplete collection, an error or no targets. Read `run.json`, exclusions and analyzed file counts. The child environment removes inherited credentials and disables metrics and version checks; it does not enforce a system network firewall.

## Additional tools

| Need | Options | Check before running |
|---|---|---|
| Data-flow analysis | Semgrep, CodeQL | Language, edition, extraction, sources/sinks and versioned rules |
| Dependencies and images | OSV-Scanner, Syft, Grype, Trivy | Resolved inventory, database date and data sent externally |
| Secrets | Gitleaks | Working tree or history, masking and exclusions |
| Infrastructure and CI | Checkov, zizmor, actionlint | Rendered values, backend/provider, scripts and events |
| Cloud and clusters | Prowler, ScoutSuite, kube-bench | Account, read identity, regions, permissions and API traffic |
| Active web tests | ZAP, Burp, Nuclei | Targets, accounts, reviewed templates, rate and permitted effects |
| Networks | Nmap, testssl.sh | Exact hosts and ports, probes, IPv6 and vantage point |
| Native code | ASan, UBSan, TSan, Miri, AFL++, libFuzzer | Isolated build, real API, corpus, watchdog and resources |
| Mobile and firmware | MobSF, JADX, Ghidra, Frida | Artifact, laboratory device and isolated extraction |
| AI | PyRIT, garak, AgentDojo | Model/version, synthetic data, simulated tools and budget |
| Smart contracts | Slither, Foundry, Echidna | Compiler, invariants and local chain |
| Detection | Sigma, YARA-X, Suricata | Engine version, ingested fields and positive/negative corpus |

Install a tool when a selected check requires it. Use the official repository and an identified version, verify licence and integrity, then read that version's help. Bundled third-party workflows are documentation references; the library does not run their scripts.

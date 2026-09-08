# Validation record: 9 September 2026

## Results

| Check | Observed result |
|---|---|
| Tool, import, assessment, distribution, package and local query tests | 70 tests run, 70 passed |
| Bundled Semgrep rules | 6 rules; 7 positive cases detected; 6 safe cases without alerts; 2 files scanned |
| Codex entry point validation | 9 skills accepted by `quick_validate.py` |
| Control schema | 58 records validated against JSON Schema draft 2020-12 |
| Catalogue and resources | Names, paths, local links, source references and hashes checked |
| Trail of Bits files | All 336 SHA-256 hashes match the lock file |
| MITRE index | Derived index identified by commit, three input bundle hashes and output hash |
| Initial references | 50 HTTP checks; all links accessible during the check |
| Upstream repositories | 22 retained repositories; maintenance metadata and declared licences recorded |
| Local installation | 9 links created to this repository, without collisions or overwrites |
| Installed entry point checks | SaaS/MCP/OT plan generated with 16 methods pointing to existing files; MITRE and Modbus queries passed |
| Final source availability | 59 references reachable across two checks; content-review scope recorded separately |
| Independent review | One synthetic service; three defects confirmed, one policy question retained; 27 local behavior checks |
| Package checks | Repeatability on identical inputs, overwrite refusal, altered files, extra members, traversal and duplicate members tested |
| Claude Code | Native client 2.1.212 validated both manifests, installed the plugin in an isolated configuration and discovered all nine skills |
| Installed Claude plugin resources | Audit plan generated from the cached plugin for a separate project; all 13 selected methods and domain entry points resolve inside the installed plugin |

Semgrep version: 1.165.0. The main commands use the Python standard library. The one-off schema and skill checks used PyYAML and jsonschema from the installed Semgrep runtime; these packages are not required for inventory or queries.

The native `semgrep --test` command failed before analysis while pairing configuration and fixture files. The local rule checker runs the scanner and compares every result with positive and negative annotations. [KB.md](KB.md) records the failure and the workaround.

## Behaviors checked

- Inventory and planning do not execute project scripts or read `.env` values.
- Symlinks and excluded directories remain outside the reported coverage.
- Truncation, parse errors and empty scans remain visible as incomplete or failed analysis.
- Imports omit secrets, raw matches and source code, and retain findings as candidates.
- Deduplication preserves distinct locations and commits.
- Report metadata cannot become active HTML or Markdown links.
- On POSIX, a scanner timeout stops its process group, including children.
- Installation supports preview, refuses collisions and is idempotent.
- MITRE and OT queries include cases that must match and cases that must return no result.
- Compiled controls match their authored sources; duplicate identifiers and missing evidence requirements are rejected.

## English documentation revision

All 68 original Markdown documents, nine skill interface descriptions, catalogue descriptions, control text and generated report labels were reviewed and rewritten in English. The control compiler now reads English method headings. Method identifiers, source URLs and the number of procedure steps were preserved.

The 40 tests, nine skill checks, 58 schema checks and 203 local link checks passed after the revision. Third-party files and the MITRE index retained their recorded hashes. These are editorial and tool checks; they do not expand the field validation described below.

## Distribution revision: 9 September 2026

Five optional repositories and their active references were removed. The MITRE registry entry now records derived data and points to the bundled provenance; validation checks its source commit and reuse classification. The source registry still contains 59 entries and is not a count of every technical URL in the documentation.

The release now includes the Claude plugin and marketplace manifests. Tests verify that a relocated archive retains these manifests and its shared resources, then run the planner from a separate target directory. Version drift, an incomplete marketplace source and incorrect MITRE reuse metadata are rejected.

Claude Code's native validator accepts the plugin with one expected warning: the root `CLAUDE.md` is a maintainer entry point and is not injected into plugin sessions. Audit instructions live in the shared skills. The marketplace validates without warnings. Installation and discovery were tested without model inference; an end-to-end audit performed by a Claude model has not been evaluated here.

Gitleaks 8.30.1 scanned the four existing Git commits across all refs before publication. Its four alerts were file hashes in the upstream lock, each verified against the corresponding file. No credential was identified in those alerts. The unchanged Semgrep rule results above were obtained on 8 September.

## Limits

The final review corrected finding identity after redaction, Windows path handling and candidate-status promotion. Additional tests cover scanner executable lookup, bounded output, assessment evidence requirements and release archives. The delivered reproduction script snapshots mutable observations before recording them, and its persisted actual/expected values are checked.

The changed local runner completed a Semgrep scan of the two rule fixture files. The six-rule test harness detected seven positive cases and left six safe cases unflagged. GitHub's workflow checks Python 3.10 and 3.13, runs the standard-library suite and builds the release archive; it does not install or run Semgrep.

These results cover local tools and specific library behaviors. The [independent review](examples/review-lab-report.md) covers one synthetic service and has no population-level detection metric. Specialist methods have not been evaluated across every possible stack. Third-party scripts and workflows have not been executed or fully audited.

No active test was run against a client endpoint, cloud account, authenticated application, live SIEM or industrial device. Additional scanners require installation, configuration and effect checks for the project concerned. Deployment behavior still requires evidence from the running system.

## Repeat the checks

```bash
python3 -m unittest discover -s tests -v
python3 scripts/test_rules.py
python3 scripts/validate_library.py
```

To check source availability again, write to a new file:

```bash
python3 scripts/check_sources.py --out /private/path/source-check.json
```

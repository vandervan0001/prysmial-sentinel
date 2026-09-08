# Validation record: 8 September 2026

## Results

| Check | Observed result |
|---|---|
| Tool, import, control and local query tests | 40 tests run, 40 passed |
| Bundled Semgrep rules | 6 rules; 7 positive cases detected; 6 safe cases without alerts; 2 files scanned |
| Codex entry point validation | 9 skills accepted by `quick_validate.py` |
| Control schema | 58 records validated against JSON Schema draft 2020-12 |
| Catalogue and resources | Names, paths, local links, source references and hashes checked |
| Trail of Bits files | All 336 SHA-256 hashes match the lock file |
| MITRE index | Derived index identified by commit, three input bundle hashes and output hash |
| Initial references | 50 HTTP checks; all links accessible during the check |
| Upstream repositories | 27 HEAD commits resolved; maintenance metadata and declared licences recorded |
| Local installation | 9 links created to this repository, without collisions or overwrites |
| Installed entry point checks | SaaS/MCP/OT plan generated with 16 methods pointing to existing files; MITRE and Modbus queries passed |

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

## Limits

These results cover local tools and specific library behaviors. Specialist methods have not been evaluated across every possible stack or through an independent agent evaluation. Third-party scripts and workflows have not been executed or fully audited.

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

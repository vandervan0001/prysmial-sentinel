# Prysmial Sentinel

Prysmial Sentinel is a cybersecurity skill library for reviewing software, infrastructure and industrial systems in Codex. It covers code review, pentesting, detection, threat hunting and incident response, with a shared format for evidence and findings.

Created by [vandervan](https://github.com/vandervan0001), as part of [Prysmial](https://prysmial.com).

The library contains nine skills: one audit coordinator and eight domains. They provide 36 specialist methods and 58 searchable controls. Local tools handle project inventory, audit planning, a limited Semgrep scan and scanner report imports. The methods guide the rest of the review.

Seven targeted guides provide test cases for authorization across jobs and caches, parser boundaries, agent permissions, release provenance, cryptographic migration, telemetry and OT recovery. A [reproducible review example](examples/review-lab-report.md) shows three defects that the bundled scanner patterns do not detect.

## Install and start

Use Python 3.10 or later. Clone the repository with an account that has access, then preview the installation and apply it:

```bash
git clone https://github.com/vandervan0001/prysmial-sentinel.git
cd prysmial-sentinel
python3 scripts/install.py
python3 scripts/install.py --apply
```

A ZIP and SHA-256 checksum are also available in the [GitHub releases](https://github.com/vandervan0001/prysmial-sentinel/releases).

The installer links the nine skills into the Codex skills directory. It refuses conflicting paths and preserves existing skills. Keep this repository in place; if you move it, recreate the links. Codex may need a new task or a skill reload to discover them.

In the project you want to review:

```text
$cyber-audit Review this project in depth. Start with the repository and local tests. Report confirmed findings, supporting evidence and checks that still require the running application.
```

You can also call a domain directly:

```text
$cyber-ot Review this architecture and these Siemens exports. Check S7 access, maintenance access, backups and segmentation.

$cyber-hunting Test this hypothesis against the supplied logs. Include a known event to check collection coverage and explain any gaps.
```

## Choose a domain

| Skill | Scope |
|---|---|
| [cyber-audit](skills/cyber-audit/SKILL.md) | Inventory the project, select methods and consolidate findings and coverage |
| [cyber-core](skills/cyber-core/SKILL.md) | Threat models, MITRE references, controls, research and evidence assessment |
| [cyber-pentest](skills/cyber-pentest/SKILL.md) | Attack surface, networks, Windows/AD, Linux and authorized active tests |
| [cyber-appsec](skills/cyber-appsec/SKILL.md) | Code, APIs, identity, cloud, CI/CD, AI/MCP/RAG, mobile, desktop, native code and cryptography |
| [cyber-detection](skills/cyber-detection/SKILL.md) | Sigma, YARA, Elastic/Splunk, telemetry and rule tests |
| [cyber-hunting](skills/cyber-hunting/SKILL.md) | Hypotheses, log queries, investigative pivots and alternative explanations |
| [cyber-purple-team](skills/cyber-purple-team/SKILL.md) | Controlled tests from observed behavior through to alert delivery |
| [cyber-dfir](skills/cyber-dfir/SKILL.md) | Endpoint evidence, suspicious files, timelines and incident response |
| [cyber-ot](skills/cyber-ot/SKILL.md) | OT/ICS architecture, protocols, firmware, vendor guidance and IEC 62443 applicability |

The [catalogue](CATALOG.md) lists each method. The [architecture](ARCHITECTURE.md) defines domain responsibilities and handoffs.

The OT domain includes Modbus, S7, PROFINET, EtherNet/IP/CIP and OPC UA, plus Siemens, Rockwell, Schneider and Omron checks. Reviews start from architecture, exports, captures and simulators. Physical tests require preparation for the specific equipment and process.

## Included tools

- Local inventory and audit plans, with file limits and exclusions recorded.
- Semgrep scans on a temporary file copy, using six bundled rules with positive and negative test cases.
- Semgrep, SARIF 2.1.0, Gitleaks and Trivy imports, with sanitized JSON and Markdown reports.
- Offline searches across MITRE ATT&CK Enterprise, ICS and Mobile, and controls filtered by domain or protocol.
- Checks for catalogue consistency, local links, skill metadata and imported file integrity.
- Assessment validation that requires supporting evidence for reviewed finding and coverage statuses.
- Versioned release archives with complete file manifests and verification without extraction.

See the [commands and limits](skills/cyber-audit/references/tooling.md). Semgrep must already be installed to run a scan. Other tools mentioned in the methods need to be selected, installed and checked for the project. Imported findings remain candidates until their cause and impact are verified.

## Validation

Local validation passed 66 tests and the Semgrep rule checks. An independent agent review exercised one synthetic service with 27 local checks. These results do not establish coverage across every stack or live client system. See the [validation record](VALIDATION.md) for the cases and environments checked.

Technical references and review history are kept in the [research notes](RESEARCH.md). [Third-party notices](THIRD_PARTY_NOTICES.md) cover bundled documentation and data.

## Creator and Prysmial

[vandervan](https://github.com/vandervan0001) created Prysmial Sentinel to organize security review methods, local tooling and evidence requirements in one repository.

[Prysmial](https://prysmial.com) builds business software and process automation, including CRMs, applications, portals and AI integrations. For project work or collaboration, contact [vandervan on LinkedIn](https://www.linkedin.com/in/tai-van/).

See [project credits](CREDITS.md) for authorship. To reference Sentinel in an article, workshop or audit, use the [citation metadata](CITATION.cff) and identify the version you used.

## Maintain the library

Edit a method in its domain, then regenerate the control catalogue and run the checks:

```bash
python3 scripts/compile_controls.py
python3 -m unittest discover -s tests -v
python3 scripts/test_rules.py
python3 scripts/validate_library.py
```

Keep raw audit evidence in a private output directory. Record untested areas in each report, including checks that require a deployed service, authenticated session or physical device.

See [contribution guidance](CONTRIBUTING.md) for method and release changes, and [SECURITY.md](SECURITY.md) for vulnerability reports and tool boundaries.

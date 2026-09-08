# Third-party notices and provenance

Project creator and upstream acknowledgements are recorded in [CREDITS.md](CREDITS.md). The notices below apply to third-party material.

## Trail of Bits

Source: [trailofbits/skills](https://github.com/trailofbits/skills), commit `d3323cefbcf645678b8dc481de204b02ad3d02dc`, retrieved on 8 September 2026. Authors: Trail of Bits and contributors. Licence: Creative Commons Attribution-ShareAlike 4.0 International. The [full licence is included](skills/cyber-audit/references/upstream/trailofbits/LICENSE).

Copied sets: constant-time-analysis, property-based-testing, variant-analysis, semgrep-rule-creator, zeroize-audit, agentic-actions-auditor, supply-chain-risk-auditor and testing-handbook-skills. They contain 336 files and 22 documentation entry points. File contents are unchanged. The 22 `SKILL.md` filenames were renamed to `SOURCE.md` to prevent discovery as additional skills. [upstream-lock.json](skills/cyber-audit/references/upstream-lock.json) records the path mapping and SHA-256 hashes.

These resources retain their attribution and licence terms. Their application-specific workflows are not automatically activated. Their scripts have not been validated or executed as part of this delivery.

## MITRE ATT&CK

© 2026 The MITRE Corporation. This work is reproduced and distributed with the permission of The MITRE Corporation.

Source: [mitre-attack/attack-stix-data](https://github.com/mitre-attack/attack-stix-data), commit `6cda5ad8462c79e14fbb872f4e09059b18e0cfc4`. [MITRE licence and disclaimers](skills/cyber-core/references/attack/LICENSE.txt).

The Enterprise, ICS and Mobile bundles were transformed into a local index. The transformation selects active objects relevant to the library, removes revoked or deprecated objects and normalizes fields. The result is not a complete STIX bundle. [provenance.json](skills/cyber-core/references/attack/provenance.json) records the sources, input hashes and transformation.

ATT&CK does not guarantee exhaustive coverage of adversary behavior. Its descriptions are reference data and do not authorize audit actions.

## Linked sources

Other repositories in the registry are research and method references. They are not distributed in full or installed automatically. GitHub licence metadata may be incomplete or return `NOASSERTION`; read the licence for the file and commit before reuse. No common licence is assigned to these projects here.

Original procedures, local rules and audit tooling are separate from these third-party snapshots.

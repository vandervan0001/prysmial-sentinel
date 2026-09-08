---
name: cyber-audit
description: "Coordinate a project security review by selecting relevant cyber methods, inventorying local files and tracking evidence, coverage and retests. Use for broad cybersecurity, AppSec or pentest requests without loading every method at once."
---

# Project security audit

Read the [audit contract](references/engagement.md). Establish scope from the request, repository and existing permissions. Start with available information. A missing answer should block only the action that depends on it.

## Start

1. Read the project instructions and KB. Identify the path, Git state, architecture and environments. The inventory reads filenames and a bounded set of manifests without executing the project.
2. Generate the inventory and plan. Replace example paths with identified absolute paths:

   ```bash
   python3 /path/skills/cyber-audit/scripts/audit.py plan /path/project --profile deep --out /private/path/plan.json
   python3 /path/skills/cyber-audit/scripts/audit.py doctor
   ```

3. Read the selected `SKILL.md` entries from the [catalogue](references/catalog.json). File-based suggestions need confirmation against the actual stack. Add missing surfaces such as infrastructure, runtime services and physical equipment.
4. Choose `quick` for an initial review, `deep` for a broader plan, or `--add cyber-ot` for a domain that files alone cannot identify. Profiles change the plan; they do not extend permissions or establish tested coverage.
5. Run the relevant checks. The local runner first previews its command:

   ```bash
   python3 /path/skills/cyber-audit/scripts/audit.py scan-local /path/project
   python3 /path/skills/cyber-audit/scripts/audit.py scan-local /path/project --execute --out-dir /private/path/new-scan
   ```

The runner uses an existing Semgrep installation and bundled rules on a file copy with size limits. It excludes symlinks and installs nothing. This scan covers a subset of the catalogue. Read the [commands and limits](references/tooling.md) before running it.

## Review and report

Keep a coverage table with object, method, evidence and status. Confirm findings by tracing the data path and trying to disprove the suspected defect. Search for variants after confirming a cause. After an authorized fix, rerun the failing scenario and a legitimate case.

Import external results with `audit.py normalize`, then record triage decisions and prepare the report using the triage method in `cyber-core`. The generated Markdown report lists candidates; complete it with verified findings and coverage.

For structured delivery, use the [assessment contract](references/assessment-format.md). Its validator checks evidence references and the support required for each status. Review the cited evidence as well; valid JSON cannot establish that an observation is true. The [synthetic review](../../examples/review-lab-report.md) shows the difference between scanner output and verified findings.

For recent changes and advisories, consult the [dated references](references/sources.json) and follow the [research method](references/research-policy.md). Selected Trail of Bits references are available with [provenance and hashes](references/upstream-lock.json).

# Reviewed assessment records

Scanner imports remain candidates. Use a separate `security-assessment` record for human or agent review decisions. Validate it with:

```bash
python3 skills/cyber-audit/scripts/assessment.py /private/path/assessment.json
```

The validator checks structure, referenced evidence and status requirements. It does not execute referenced files, verify their content or authenticate the reviewer. A fabricated observation can still satisfy a data contract. Review the evidence itself before relying on the assessment.

## Fields

The root contains `schema_version: 1`, `kind: "security-assessment"`, `target`, `evidence`, `controls`, `findings` and `limitations`.

- `target`: name, revision or artifact identifier, environment and scope.
- `evidence`: records with a unique ID, kind, source, SHA-256 of collected bytes and a short observation. Keep raw evidence private; paths and hashes are references, not instructions to fetch or execute.
- `controls`: unique IDs, asset, method, status and evidence IDs. Use local control IDs or versioned external requirements after checking the requirement text.
- `findings`: unique IDs, title, status, control IDs and evidence IDs. Scanner severity does not determine the reviewed priority.
- `limitations`: unverified surfaces and collection limits. Include the actual environment represented by the evidence.

## Status requirements

| Status | Required support |
|---|---|
| Control `tested` | Evidence, positive case count, method, positive control, expected/observed result and `outcome` of pass, fail or mixed |
| Control `partial` | Evidence and the remaining coverage gap |
| Control `not-tested`, `blocked`, `not-applicable` | A reason specific to this asset and scope |
| Finding `candidate` | Control association; no automatic confirmation |
| Finding `confirmed` | Evidence, mechanism, preconditions, impact, attempt to disprove and remediation |
| Finding `rejected` | Evidence and rejection reason |
| Finding `needs-context` | Missing context or unresolved interpretation |
| Finding `fixed` | Confirmed-finding fields plus the correction revision |
| Finding `retested` | Correction revision, retest evidence, executed cases, legitimate control, expected/observed results and passing outcome |

For tests and retests, `execution` or `retest` contains `cases_run`, `method`, `positive_control`, `expected` and `observed`. Retests also contain `outcome: "pass"` and reference `retest_evidence`. A failed correction leaves the defect confirmed or unresolved; record the failed retest in evidence.

`tested` describes coverage. A tested control can fail. Report counts by status and retain the scoped denominator; do not convert them into a universal security score.

The [synthetic assessment](../../../examples/assessment.json) shows three confirmed defects alongside working controls. Its green format check does not mean that the reviewed application is safe.

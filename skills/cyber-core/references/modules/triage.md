# Finding triage and reporting

## Procedure

1. Validate imported formats and each scanner execution status. Report errors, timeouts, partial analysis and zero analyzed objects even when there are no findings.

2. Try to disprove each priority candidate: constant input, upstream validation, inaccessible route, fixed variant, required prior permission or inapplicable scenario.

3. Confirm the path and impact, or retain `needs-context`. Keep the decision open when evidence is missing. Group duplicates without losing distinct sources or locations.

4. Set priority according to exposure and business effect. If CVSS is required, calculate the vector and document its assumptions; do not copy a score from a superficially similar issue.

5. Report priority findings, fixes, tests and coverage. Volume metrics do not establish audit depth. Justify each `not-applicable` control.

## Required evidence

A confirmed finding must let another reviewer locate the evidence. Preserve original scanner status, triage decisions and untested controls in the report.

## Tools and limits

The local importer accepts Semgrep JSON, SARIF, Gitleaks and Trivy JSON. It removes raw excerpts and keeps findings as candidates. Inspect raw evidence under restricted access where needed.

## References

- [FIRST CVSS](https://www.first.org/cvss/v4.0/specification-document): 4.0.
- [FIRST EPSS](https://www.first.org/epss/): Retrieve a dated score for each CVE.
- [MITRE CWE](https://cwe.mitre.org/): Verify each identifier.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

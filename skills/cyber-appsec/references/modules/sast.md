# Static analysis and rules

## Procedure

1. Choose syntax, taint or interprocedural analysis for the defect under review. Check capabilities of the available version and edition; an installed CLI alone does not establish cross-file analysis support.

2. Run local rules against an identified snapshot. Record versions, rules, analyzed and excluded files, parse errors and timeouts. Do not load unreviewed rules from the target repository.

3. For compiled CodeQL analysis, verify that the database contains the intended targets and translation units. Isolate the build without production secrets. Starting an extractor does not prove useful code was captured.

4. Build a rule from an understood defect: source, transformations, sink and an effective sanitizer. Add vulnerable and safe cases, aliases, wrappers and relevant syntax variants. Verify the protection before treating a validator as a sanitizer.

5. Import results with execution metadata. Group by cause and location carefully, keeping source rules and explicit reasons for rejected findings.

## Required evidence

A custom rule must detect its vulnerable cases and leave safe controls unflagged. Report analyzed file counts, parse errors and missing coverage.

## Tools and limits

The library provides a local Semgrep runner and targeted rules for a limited set of constructs. Add maintained, reviewed rule packs according to the project. Treat SARIF input as untrusted data.

## Bundled reference

Read the [Trail of Bits method](../../../cyber-audit/references/upstream/trailofbits/plugins/semgrep-rule-creator/skills/semgrep-rule-creator/SOURCE.md) when needed. The [provenance lock](../../../cyber-audit/references/upstream-lock.json) records the snapshot and licence. Adapt Claude-specific tools and workflows to the available environment. Reading this reference does not authorize running its scripts or invoking its agents.

## References

- [Semgrep documentation](https://semgrep.dev/docs/running-rules): Match the installed CLI.
- [GitHub CodeQL](https://docs.github.com/en/code-security/reference/code-scanning/workflow-configuration-options): Workflow options.
- [Trail of Bits skills](https://github.com/trailofbits/skills): Snapshot recorded in upstream-lock.json.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

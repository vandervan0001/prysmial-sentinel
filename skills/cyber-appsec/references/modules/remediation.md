# Remediation and retesting

## Procedure

1. Read existing checks and shared workspace context. Save a comparison copy before editing; do not use Git to restore an entire shared file when undoing a local mutation.

2. Fix the component that enforces authority or owns the data. Correct related paths affected by the same cause without expanding into an unrelated refactor.

3. Write a test that reaches the defect and an authorized scenario that must still succeed. Require a nonzero executed test count as well as the expected exit code.

4. Run the test before and after the fix on identified versions. For mutation checks, use an isolated copy, unique anchors and a restoration check; disable Python bytecode when needed.

5. Run the build and relevant checks. Record the fixed source, built artifact, deployment and runtime behavior separately. A local fix does not close an exposure still active remotely.

## Required evidence

Provide the targeted diff, before/after evidence, effect on authorized behavior, variants addressed and remaining delivery step. Use `retested` only after rerunning the check against the identified fix.

## Tools and limits

Use tests in the shipped runtime and the project tooling. Understand the business effect before changing failing expectations. Preserve neighboring work.

## References

- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/): 5.0.0.
- [Trail of Bits skills](https://github.com/trailofbits/skills): Snapshot recorded in upstream-lock.json.
- [GitHub CodeQL](https://docs.github.com/en/code-security/reference/code-scanning/workflow-configuration-options): Workflow options.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

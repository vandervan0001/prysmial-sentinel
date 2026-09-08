# CI/CD and development agents

## Procedure

1. Trace data from pull requests, issues, branches and artifacts into shells, templates, agents and builds. Passing data through an environment variable does not make it trusted.

2. Review pull_request_target, workflow_run and bot commands against the commit actually checked out. Job chaining must not give an untrusted branch secrets or a write token.

3. Check least-privilege permissions, protected environments, OIDC, persistent runners, caches and artifacts. Verify provenance rather than relying on the presence of an attestation.

4. For AI agents, trace untrusted input, available capabilities, secrets, outbound access and the final action. Verify that review or approval covers the exact bytes and target executed.

5. Verify that CI builds the deployed artifact and runs type checks and relevant tests with a nonzero case count. Passing tsc does not prove the build succeeds; a build does not prove type checks pass.

## Required evidence

Provide the event → data → privileged step path and identify the code executed. Use synthetic receivers in place of external actions for local demonstrations.

## Tools and limits

Use YAML review, actionlint, zizmor and CodeQL where available. Pin actions and dependencies according to the project maintenance policy. Do not trigger a privileged workflow to test a hypothesis.

## Bundled reference

Read the [Trail of Bits method](../../../cyber-audit/references/upstream/trailofbits/plugins/agentic-actions-auditor/skills/agentic-actions-auditor/SOURCE.md) when needed. The [provenance lock](../../../cyber-audit/references/upstream-lock.json) records the snapshot and licence. Adapt Claude-specific tools and workflows to the available environment. Reading this reference does not authorize running its scripts or invoking its agents.

## References

- [GitHub Actions security](https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions): Software delivery.
- [SLSA](https://slsa.dev/spec/v1.1/): 1.1; versioned reference, not a claim of the latest release.
- [Trail of Bits skills](https://github.com/trailofbits/skills): Snapshot recorded in upstream-lock.json.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

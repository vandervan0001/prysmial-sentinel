# Infrastructure as code

## Procedure

1. Trace variables and module outputs to rendered resources. Distinguish values unknown at plan time from values demonstrated to be permissive.

2. Look for public exposure, broad permissions, disabled logging, encryption settings and network policies. Relate each rule to provider behavior and justified exceptions.

3. Review state backends, locking, access, versions and secrets. State and plan files can contain sensitive values even when the interface masks them.

4. Check module origins, provider versions, checksums and external data sources. Producing a plan can execute providers and external data programs; use an appropriate isolated environment.

5. Prepare a diff and describe its resource effects. Compare it with deployed state to assess drift when access is available. Do not apply a plan solely to confirm a rule finding.

## Required evidence

Provide the resource address, resolved value, environment context and provider control. Mark the result partial when sensitive or dynamic values prevent a decision.

## Tools and limits

Use Checkov, Trivy config and versioned policy-as-code rules. Review suppressions and their justification. Treat plan output as sensitive evidence.

## References

- [Trivy](https://trivy.dev/latest/docs/): Check the installed version.
- [AWS IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html): IAM.
- [Kubernetes security checklist](https://kubernetes.io/docs/concepts/security/security-checklist/): Match the cluster version.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

# Cloud and service identities

## Procedure

1. Start from IaC exports and policies. Where cloud access is authorized, verify the account identity before querying and record collection date, region and permissions.

2. Reconstruct effective permissions, trust relationships, delegation and ways to modify a more privileged identity. Assess broad roles against their trust policies and organization-wide constraints.

3. Review workload federation and CI OIDC: audience, subject, repository, branch or environment, and duration. Check rotation and removal of long-lived keys.

4. Relate network exposure, public storage, encryption keys, logs and backups to the business asset. Resources missing from an incomplete regional inventory remain unverified.

5. Compare deployed and declared state, then simulate or prepare targeted changes. A Terraform plan does not establish effective permissions or account state.

## Required evidence

Provide the principal → permission → resource → effect chain with a dated policy export. List regions, services and accounts that were not inspected.

## Tools and limits

Prowler, ScoutSuite and IAM simulators depend on provider and version. Collectors make API calls and require permissions; do not use administrator credentials for convenience.

## References

- [AWS IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html): IAM.
- [Microsoft identity management](https://learn.microsoft.com/en-us/azure/security/fundamentals/identity-management-best-practices): Azure and Entra.
- [Google service account keys](https://docs.cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys): IAM.
- [SLSA](https://slsa.dev/spec/v1.2/): 1.2; approved specification, source and build tracks.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

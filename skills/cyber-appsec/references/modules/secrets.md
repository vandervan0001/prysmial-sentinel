# Secrets and credentials

## Procedure

1. Define the inspected storage locations before searching. A working-tree scan does not cover Git history, CI caches or image layers.

2. Use sanitized output. Keep secret type, file, line, commit and a non-reversible fingerprint of the relevant signal. Never print a secret to prove its presence.

3. Distinguish synthetic fixtures, public keys, non-secret identifiers and plausible credentials. Testing a token against its provider requires permission for that use.

4. Trace provisioning, permissions, lifetime, rotation, revocation, backups and logs. Check behavior when a secret is missing, expired or renewed.

5. For confirmed exposure, prepare revocation and replacement before history cleanup. Check invalidation of derived sessions or tokens. Removing data from Git does not revoke credentials.

## Required evidence

Identify the storage location and exposure path without disclosure. Rotation evidence must cover both the configured replacement and actual invalidation of the old credential.

## Tools and limits

Use Gitleaks or an equivalent scanner with masking. Give false-positive exclusions a specific justification and expiry where temporary. Avoid global extension-based exclusions.

## References

- [Gitleaks](https://github.com/gitleaks/gitleaks): External tool reference.
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/): Read the relevant guide.
- [AWS IAM best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html): IAM.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

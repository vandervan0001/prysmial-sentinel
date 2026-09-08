# Images and containers

## Procedure

1. Compare source files with the final image. Review multi-stage copies, users, entrypoints, dependencies and artifacts left in earlier layers.

2. Look for secrets passed through ARG/ENV, build files, caches or layer history. Deleting a secret in a later layer leaves it in the original layer.

3. Check the base image digest, updates, signature and SBOM for the delivered image. Review the signature verifier trust policy: expected identity, issuer and provenance.

4. Relate capabilities, seccomp, UID, mounts, Docker socket access and resource limits to the actual risk. A non-root container with a privileged socket may retain extensive access.

5. Test shutdown, signals, temporary files and missing configuration in an isolated runtime. Keep the host socket and real credentials outside the laboratory.

6. Use the [targeted verification cases](../supply-chain-verification.md) when this surface is present. Select cases for the actual architecture and record the observed limits.

## Required evidence

Provide the digest, platform, relevant layer or configuration, and effect. A Dockerfile scan does not establish the contents of the distributed image.

## Tools and limits

Use Trivy, Syft, Grype, OCI inspection and signing tools. Extract untrusted images without starting them or following links into the host filesystem.

## References

- [Trivy](https://trivy.dev/latest/docs/): Check the installed version.
- [SLSA](https://slsa.dev/spec/v1.2/): 1.2; approved specification, source and build tracks.
- [Kubernetes security checklist](https://kubernetes.io/docs/concepts/security/security-checklist/): Match the cluster version.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

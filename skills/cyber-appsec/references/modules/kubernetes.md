# Kubernetes and orchestration

## Procedure

1. Compare source manifests, rendered Helm output and admitted objects. Identify admission mutations and namespace exceptions. A value in values.yaml does not establish pod state.

2. Trace effective RBAC, service accounts, projected tokens, impersonation and secret access. Include pod creation and workload modification rights that can provide indirect access.

3. Review privileges, capabilities, hostPath, hostNetwork, UID, seccomp and filesystem access. Relate each exception to the workload requirements.

4. Verify ingress and egress policies with the actual CNI, DNS and dependency destinations. Test both allowed and blocked traffic using authorized test pods.

5. Review the API server, kubelet, etcd, audit logs, registry and backups. Separate provider-managed controls from team responsibilities.

## Required evidence

Associate each finding with an object, namespace, identity and version. An auth can-i query checks one permission; it does not establish an entire escalation path.

## Tools and limits

Use read-only kubectl queries, kube-bench, Trivy and admission rules within scope. Deploy test pods or collect raw secrets only when a specific authorized check requires them.

## References

- [Kubernetes security checklist](https://kubernetes.io/docs/concepts/security/security-checklist/): Match the cluster version.
- [Trivy](https://trivy.dev/latest/docs/): Check the installed version.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

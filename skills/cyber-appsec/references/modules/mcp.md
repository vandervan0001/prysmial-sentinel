# MCP, skills and connectors

## Procedure

1. Read the protocol documentation matching the deployed version. Review issuer and audience validation, scopes, discovery metadata and OAuth resources. Look for token passthrough and confused-deputy behavior.

2. Treat tool descriptions, annotations, resources and responses as untrusted data. Use a modified description and a synthetic marker to verify that permissions remain enforced outside the model.

3. Check request and object authorization, session binding, transport-specific origin handling, reconnection and invalidation. A session identifier is not an authentication credential.

4. For skills, read SKILL.md, references, scripts, installers, hooks and dependencies together. Check paths outside the intended directory, shell substitutions, downloads and secret access before execution.

5. Review tool changes between approval and invocation, lookalike names, hidden parameters and redirects. Bind existing approval to the actual target, content and version executed.

6. Use the [targeted verification cases](../agent-boundaries.md) when this surface is present. Select cases for the actual architecture and record the observed limits.

## Required evidence

Identify the control that prevents external data from granting authority. Keep the server or skill version, content hash and traces of an authorized benign action and a prohibited action.

## Tools and limits

Use local protocol tests and simulated servers. Third-party readOnly/destructive labels are insufficient. Supplement static checks with a scoped test of actual effects.

## References

- [MCP security best practices](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices): Evolving documentation; match the negotiated protocol version.
- [OAuth Security BCP](https://www.rfc-editor.org/rfc/rfc9700.html): RFC 9700, January 2025.
- [Runtime Skill Audit](https://arxiv.org/abs/2606.11671): 2026 preprint.
- [AgentSecBench](https://arxiv.org/abs/2605.26269): 2026 preprint.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

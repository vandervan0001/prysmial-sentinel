# Threat modeling

## Procedure

1. Reconstruct flows from routes, message consumers, scheduled jobs and administrative access. Associate each trust boundary with a concrete mechanism: session, token, network, process or signature.

2. Distinguish anonymous actors, users from two organizations, support staff, administrators, compromised suppliers and code executed during delivery. A business organization does not necessarily map to a technical tenant boundary.

3. Write testable invariants: who can read which object, change which transition or delegate which capability. Include exports, caches, search, backups and job queues alongside HTTP routes.

4. Trace three to five priority scenarios from accessible input to effect: cross-user reads, privilege escalation, repeated actions, transitive trust or state corruption. Keep hypotheses distinct from demonstrated defects.

5. Associate each scenario with an existing control, its location and a planned check. Record assumptions supporting the conclusion and those requiring runtime observation.

## Required evidence

Provide a flow diagram, an actor × operation × data matrix and prioritized scenarios with their existing checks, available evidence and missing tests.

## Tools and limits

Use Mermaid for a small diagram. STRIDE helps explore threats, but a category alone does not establish risk. Match the model to the observed repository and environment.

## References

- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/): 5.0.0.
- [MITRE ATT&CK](https://attack.mitre.org/): Cite technique and version.
- [MITRE ATLAS](https://atlas.mitre.org/): AI taxonomy.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

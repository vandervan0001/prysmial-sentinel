# Incident response and evidence

## Procedure

1. Preserve available evidence with source, time, timezone, hash and collection method. Work on copies and distinguish observations, hypotheses and missing data.

2. Build a correlated timeline of identities, access, deployments and changes. Check clock offsets and collection gaps before inferring causation.

3. Define confirmed scope and possible extensions. Missing exfiltration traces are inconclusive when telemetry could not observe the transfer.

4. Prepare proportionate containment for affected sessions, keys, resources and dependencies. Explain effects and rollback before any action that could interrupt service.

5. Verify recovery from a clean source, required rotations, restored controls and monitoring. Restarting a service does not establish that the cause was removed.

## Required evidence

Provide the timeline, confidence, evidence, alternative explanations, completed actions and pending decisions. Separate containment recommendations from actions actually taken.

## Tools and limits

Use log analysis, cloud exports and disk images within the mandate. A diagnostic request alone does not authorize evidence deletion, reinstallation or access revocation.

## References

- [NIST incident response](https://csrc.nist.gov/pubs/sp/800/61/r3/final): 800-61 rev. 3.
- [MITRE ATT&CK](https://attack.mitre.org/): Cite technique and version.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

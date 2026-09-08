# OT, ICS and control systems

## Procedure

1. Establish physical consequences, fallback modes and availability dependencies from the supplied context. Distinguish control, supervision and safety functions.

2. Trace maintenance access, engineering workstations, backups, vendor accounts and IT/OT transfers. Review zones, permitted flows and ways to observe their use.

3. Review controller/HMI exports and communication settings: remote writes, passwords, critical commands, readback, versioning and restoration. Do not load a change into equipment merely to verify it.

4. Use existing captures and simulators for industrial protocols. Assess authenticity, replay, limits and command consistency on a bench disconnected from the process.

5. Prepare physical intervention only with an operating window, operator, restorable backup, monitoring and suitable stop procedure. A tool labeled passive may still send traffic to the controller.

## Required evidence

Provide access paths, documented gaps, potential process effects and required follow-up checks. Identify whether evidence comes from an offline export, simulator or physical equipment.

## Tools and limits

Use PCAP analysis, vendor documentation and NIST SP 800-82 rev. 3. Active scans, restarts, register writes and controller load tests are outside the default review.

## References

- [NIST OT security](https://csrc.nist.gov/pubs/sp/800/82/r3/final): 800-82 rev. 3.
- [MITRE ATT&CK](https://attack.mitre.org/): Cite technique and version.
- [NIST incident response](https://csrc.nist.gov/pubs/sp/800/61/r3/final): 800-61 rev. 3.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

# Detection and telemetry

## Procedure

1. Start with the behavior to observe and its preconditions. Map ATT&CK or ATLAS techniques to data sources actually ingested.

2. Review collection, timestamps, identity, enrichment, normalization and retention. Fields in source logs may disappear before correlation.

3. Write rules against stable fields and relevant variants. Add positive and benign events, then test backend conversion and actual query syntax.

4. Measure matches, false positives and volume in an identified corpus. For YARA, assess string cost and engine limits; for network rules, assess direction, protocol and flow state.

5. Test event → rule → alert → notification using authorized synthetic data. A matching query does not prove the operator received an alert.

6. Use the [targeted verification cases](../telemetry-validation.md) when this surface is present. Select cases for the actual architecture and record the observed limits.

## Required evidence

Provide the rule, engine version, sanitized corpus, positive and negative cases, and alert delivery stage actually verified. Record missing fields as gaps in coverage.

## Tools and limits

Use Sigma, YARA-X, Suricata and the selected SIEM. Use harmless markers; keep existing malicious samples isolated and do not execute them to test a static rule.

## References

- [Sigma rules](https://github.com/SigmaHQ/sigma): External detection reference.
- [Suricata documentation](https://docs.suricata.io/en/latest/): Match the deployed engine.
- [MITRE ATT&CK](https://attack.mitre.org/): Cite technique and version.
- [MITRE ATLAS](https://atlas.mitre.org/): AI taxonomy.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

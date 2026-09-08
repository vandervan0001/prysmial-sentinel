# Hypothesis-driven investigation

Start with a hypothesis that evidence could disprove, such as unusual use of an administration capability across a group of hosts. State what would make you reject it and which data could test it.

1. Define population, period, timezone, expected behavior and suspicious signal. Consult the [local ATT&CK reference](../../cyber-core/references/domain.md) for context without inventing group attribution.
2. Establish telemetry requirements: event, fields, source, delay, retention and known losses. Find a known legitimate event before searching for missing or rare events.
3. Build the smallest query that selects the population. Add filters one at a time, record counts and document exclusions. A query selecting zero hosts cannot disprove the hypothesis.
4. Pivot on new observations: account, host, parent process, hash, domain or sequence. Limit collection to relevant evidence. Distinguish statistical anomalies, suspicious behavior and evidence of an incident.
5. Check legitimate administration, recent changes and collection failures as alternative explanations. Keep explained false positives and unresolved hypotheses.
6. Record the result, confidence, coverage and next check. Send incident evidence to DFIR. Send repeatable detections to `cyber-detection` with fixtures and noise measurements.

[ThreatHunter-Playbook](https://github.com/OTRF/ThreatHunter-Playbook) provides investigation methods, data and notebooks. Review notebooks as code before execution. Agent documentation alone does not establish that an upstream skill is complete, compatible or verified in this environment.

Deliver the hypothesis, population, queries, counts at each step, sanitized evidence, alternative explanations and decision. Exploring supplied logs requires no active scan.

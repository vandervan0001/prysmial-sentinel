# Security research

## Procedure

1. Start with vendor documentation and advisories, then standards, source code and research. Record document version, publication date and access date separately.

2. Verify affected ranges, fixes, vulnerability aliases and preconditions. Match the component and version before applying a product CVE.

3. For tools, review licence, maintenance, mechanism, limitations and installation. Pin reused code and inspect dependencies before running it.

4. Distinguish peer-reviewed research, preprints, documentation and commercial claims. Examine tasks, metrics, baselines, controls, costs and available reproduction code.

5. Turn relevant results into project-specific checks. Preserve contradictions and missing data; benchmark performance does not establish local protection.

## Required evidence

Write a short note with primary links, dates, versions, the supported claim and its effect on the audit. Mark blocked or missing sources as unverified.

## Tools and limits

Start from [sources.json](../../../cyber-audit/references/sources.json), then refresh time-sensitive information. HTTP checks establish neither scientific validity nor repository security.

## References

- [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog): Updated catalogue.
- [FIRST EPSS](https://www.first.org/epss/): Retrieve a dated score for each CVE.
- [Trail of Bits skills](https://github.com/trailofbits/skills): Snapshot recorded in upstream-lock.json.
- [AgentDojo paper](https://arxiv.org/abs/2406.13352): 2024; check revisions.
- [Indirect Prompt Injections: Are Firewalls All You Need, or Stronger Benchmarks?](https://arxiv.org/abs/2510.05244): 2025; evaluation metric critique.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

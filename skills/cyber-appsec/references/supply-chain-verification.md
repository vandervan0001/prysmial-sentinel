# Verify what gets released

Use this procedure for dependencies, build pipelines, images, firmware and update clients. Identify the artifact consumers actually receive before interpreting repository checks.

## Artifact identity

Record source repository, commit, dependency resolution, builder, build configuration, platform and final artifact digest. Compare the distributed artifact with the one tested. An SBOM describes components; its completeness and relationship to that digest require verification.

Verify attestations against expectations established independently of the artifact: trusted issuer and builder identity, intended source, subject digest, build type and accepted parameters. Check invalid signatures, a different artifact and an unexpected builder as negative cases. State the trust root and its distribution path. SLSA 1.2 separates source and build requirements; assign a track and level only after checking its requirements. [SLSA 1.2](https://slsa.dev/spec/v1.2/), [artifact verification](https://slsa.dev/spec/v1.2/verifying-artifacts).

## Advisory decisions

| Decision | Evidence required |
|---|---|
| Component is present | Resolved package identity, platform and path in the shipped artifact |
| Version is affected | Dated vendor advisory or ecosystem record, aliases and backport context |
| Vulnerable behavior is reachable | Enabled feature and call/configuration path, or an explicit unresolved status |
| Finding is not applicable | Product-specific reasoning that can be revisited after a version or configuration change |
| Fix is delivered | Corrected artifact digest and a retest of the affected path |

A VEX statement is a supplied assessment. Record its issuer, product/version match, status, rationale and date; do not let an unverified statement silently suppress evidence. EPSS is a dated population-level exploitation forecast for a CVE. KEV records known exploitation. Neither measures this application's business impact or replaces component matching. [FIRST EPSS](https://www.first.org/epss/), [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog).

## Release and update failure modes

Test wrong source, substituted artifact, stale metadata, interrupted download and downgrade handling according to the update design. Inspect who can change the workflow, verifier policy and release assets. Hashes distributed beside an archive detect accidental corruption; a party able to replace both can generate matching hashes.

Use NIST SSDF 1.1 as the published lifecycle baseline. SSDF 1.2 is listed as a draft at this review date. Record the distinction when considering its proposed changes. The GenAI SSDF profile addresses model development; select only practices applicable to the system under review. [NIST SSDF publications](https://csrc.nist.gov/Projects/ssdf/publications), [SP 800-218A](https://csrc.nist.gov/pubs/sp/800/218/a/final).

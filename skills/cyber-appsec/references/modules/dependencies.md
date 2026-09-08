# Dependencies and software supply chain

## Procedure

1. Build the resolved component inventory, including transitive dependencies, copied binaries and libraries in the final image. Compare manifests, lockfiles, SBOMs and distributed artifacts.

2. Match security advisories to exact versions and ecosystems, including CVE/GHSA aliases and vendor fixes. A backport can fix a vulnerability without adopting the upstream version number.

3. Assess reachability, enabled features, development/build/runtime context, privileges and exposure. Keep reachability unresolved when evidence is missing.

4. Check installation scripts, provenance, maintainers and publication permissions using dated records. An unavailable measurement must remain unknown rather than becoming a risk indicator.

5. Prioritize a CVE using local impact, KEV, a dated EPSS score and an applicable fix. Prepare the smallest update with build and retest of affected paths, without rewriting the whole lockfile.

6. Use the [targeted verification cases](../supply-chain-verification.md) when this surface is present. Select cases for the actual architecture and record the observed limits.

## Required evidence

For each affected component, record resolved identity, presence, sourced vulnerable version range, usage context, fix and limits. A raw CVE list remains a candidate inventory.

## Tools and limits

OSV-Scanner, Syft, Grype and Trivy are options. Some queries send component names and versions externally; use local databases or established sharing permission for private dependencies.

## Bundled reference

Read the [Trail of Bits method](../../../cyber-audit/references/upstream/trailofbits/plugins/supply-chain-risk-auditor/skills/supply-chain-risk-auditor/SOURCE.md) when needed. The [provenance lock](../../../cyber-audit/references/upstream-lock.json) records the snapshot and licence. Adapt Claude-specific tools and workflows to the available environment. Reading this reference does not authorize running its scripts or invoking its agents.

## References

- [OSV-Scanner](https://google.github.io/osv-scanner/): Check the installed version and output format.
- [Trivy](https://trivy.dev/latest/docs/): Check the installed version.
- [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities-catalog): Updated catalogue.
- [FIRST EPSS](https://www.first.org/epss/): Retrieve a dated score for each CVE.
- [SLSA](https://slsa.dev/spec/v1.2/): 1.2; approved specification, source and build tracks.
- [OpenSSF Scorecard](https://github.com/ossf/scorecard): Maintenance indicators; not proof of security.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

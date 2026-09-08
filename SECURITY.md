# Security reports and tool boundaries

Report defects in Sentinel's tools, evidence handling or audit instructions with the affected version, expected behavior, observed result and a minimal synthetic reproduction. Do not include credentials, raw customer code or live exploit data in a public issue.

For sensitive details, agree on a private channel with [vandervan](https://github.com/vandervan0001) through [Prysmial](https://prysmial.com). If a private channel is unavailable, an issue can request contact without disclosing the technical details. No response deadline or bounty is promised.

## What the tools do

The default workflow reads local files and creates plans. Active tests require the scope described in the audit contract. The Semgrep runner copies bounded inputs, removes inherited credentials, rejects project-local executable paths and limits runtime and output. This is not an OS security sandbox. Unknown tools, hostile filesystems and target builds need separate isolation.

Raw scanner output may contain sensitive data. New evidence files use restricted permissions and refuse overwrites; protect their parent directory and storage as well. Filtered metadata can still reveal names or locations. Review it before sharing.

Assessment validation checks referenced records and status requirements. It cannot authenticate an observation, verify a claimed fix or grant test permission. A passing validator may accompany an assessment with confirmed vulnerabilities.

## Release trust

Use an identified release or commit and inspect its source. ZIP manifests and SHA-256 files detect content changes relative to expected bytes. They do not authenticate a publisher who can replace both files. Sentinel currently publishes no independent signing identity or SLSA level claim.

The [validation record](VALIDATION.md) states the environments and cases tested for this release. Earlier releases retain their original artifacts. A local test result does not establish the behavior of a deployed application or an industrial device.

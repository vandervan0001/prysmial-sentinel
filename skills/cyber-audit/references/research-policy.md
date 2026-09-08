# Updating references

The initial baseline is 8 September 2026. `sources.json` separates published standards, evolving documentation, repositories and research. Record access dates separately from publication dates. `upstream-lock.json` identifies the bundled third-party file contents.

At the start of an audit, check vendor advisories for the deployed versions, then OSV/GHSA, KEV and applicable standard errata. For API and CLI options, read the installed version's help before adapting a command. Library examples do not pin the target software version.

For AI research, compare a specification with a reproducible evaluation. Record model, version, budget, dataset, attacks, benign tasks, metrics, costs and limitations. Benchmark scores do not establish the product's protection rate. Keep preprints identified as research.

Before importing a repository, review owner, activity, relevant history, licence, dependencies and installation scripts. Pin a full commit, preserve licence and attribution, read the diff and run relevant tests in an isolated directory. GitHub stars do not establish quality. Do not use `curl | sh` or automatically update target code or imported resources.

`scripts/check_sources.py` checks links and records HTTP status on request. It does not assess scientific validity or update third-party files. Mark a `403` or timeout as unverified access for that check.

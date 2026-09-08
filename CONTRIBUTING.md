# Contributing

Start with the smallest change that improves a review decision or reproduces a tool defect. Read [AGENTS.md](AGENTS.md), [KB.md](KB.md) and the [audit contract](skills/cyber-audit/references/engagement.md).

## Methods and references

Keep the nine skill entry points. Put conditional detail in an existing domain and link it from the method that needs it. A new check should identify the applicable surface, expected property, evidence, legitimate control and limits.

For a source update, record publication or revision date separately from access date. Prefer primary documentation and inspectable research. State whether you read a publication record, relevant sections or an implementation. Preserve preprint and draft status. Use [the literature review](LITERATURE_REVIEW.md) as an example.

Before copying third-party content, verify reuse terms and preserve attribution. Update provenance and hashes when the copied bytes change. Links to external code do not authorize its execution. Original Sentinel material currently has no general open-source licence grant; do not infer one from bundled third-party licences.

Keep creator credits focused on Sentinel and redistributed third-party material. General background reading does not need a credit entry. In methods and research notes, retain citations that identify an external requirement, substantiate a research claim or document material reuse. Rewriting licensed material does not by itself remove its attribution or other licence conditions.

## Code and evidence

Use synthetic fixtures without credentials, real customer records or live provider configuration. Tests should demonstrate an observable behavior and include a case that would distinguish failure from success. Keep intentionally vulnerable fixtures under `tests/fixtures/` and identify their purpose.

After changing a method or tool:

```bash
python3 scripts/compile_controls.py
python3 -B -m unittest discover -s tests -v
python3 scripts/validate_library.py
```

After changing a Semgrep rule, also run `python3 scripts/test_rules.py` with an identified Semgrep installation. The GitHub workflow runs standard-library tests and package validation; scanner execution remains a separate local check.

For a release, update `VERSION`, describe the observed checks in [VALIDATION.md](VALIDATION.md), then build into a new directory:

```bash
python3 scripts/package_library.py build --out-dir /private/path/new-release
python3 scripts/package_library.py verify /private/path/new-release/prysmial-sentinel-0.3.0.zip
```

Archive verification checks content integrity without extraction. Use `--sha256` with a digest obtained through a trusted channel when checking an expected release. Repeatable bytes assume the same compression implementation; reproducibility is tested locally on identical inputs.

Claude Code uses the shared skill directory through `.claude-plugin/plugin.json`. Keep its version aligned with `VERSION`. Validate both manifests with `claude plugin validate .claude-plugin/plugin.json` and `claude plugin validate .claude-plugin/marketplace.json` when changing plugin metadata.

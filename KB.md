# Rules from observed failures

Record reusable lessons from actual development and usage failures here. Keep design requirements and working instructions in `AGENTS.md` and the audit contract.

- **When the upstream rule test harness fails before analysis, test with the scanner and annotated cases.** Semgrep 1.165.0 raised `IndexError` while pairing configuration and fixtures under `--test`, including in a shared temporary directory. JSON scanning worked. `scripts/test_rules.py` compares all findings with positive and negative annotations and requires a nonzero scanned file count. A harness crash cannot count as a successful rule test.
- **Derive each module's identity from its own path during catalogue migrations.** A reused loop variable assigned the final slug, `research`, to all 36 entries even though their files had moved correctly. Link checks and duplicate control ID checks exposed the mistake. Verify name, path and uniqueness together.
- **Use GitHub licence metadata as an index; read the licence before copying.** The reviewed repositories reported MIT, CC, GPL, AGPL and NOASSERTION. The Semgrep Rules License is not MIT. Keep content with unverified terms as a reference until its reuse conditions are established.

- **Fingerprint findings before redacting or truncating their display labels.** Two distinct remote locations became one candidate because both rendered as the same omitted-location label. Keep a digest of original identity fields while displaying only filtered metadata.
- **Keep reviewed decisions separate from scanner imports.** The candidate report renderer accepted a manually changed `confirmed` status without any review evidence. It now rejects promoted imports; assessment records require evidence and status-specific fields.
- **Freeze observations when recording a test result.** The synthetic review harness retained a reference to an empty effect list, then later appended to that list. Its stored observation changed while its earlier `passed` boolean stayed true. Copy mutable observations and verify persisted actual/expected values as well as the summary count.

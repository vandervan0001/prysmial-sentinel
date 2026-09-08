# Fuzzing and property tests

## Procedure

1. Call the real product functions. Use a known input to verify that the harness reaches useful processing and that format rejections do not consume the whole campaign.

2. Choose coverage-guided fuzzing for native code, structured generation for objects and stateful tests for workflows. Add a dictionary or grammar where the format prevents entry into useful branches.

3. Define properties independently of the implementation: conservation, justified monotonicity, round trips over a defined domain, permission isolation or agreement with a reference implementation.

4. Set seed, initial corpus, version, timeout and memory limits. Measure executions, useful coverage, rejections, harness failures and crashes. Reproduce a crash outside the fuzzer before assessing it.

5. Minimize counterexamples and turn them into regression tests. To verify an assertion, disable the relevant check in an isolated copy and confirm that the test fails for the expected reason.

## Required evidence

Provide the harness, invariant, seed, minimal corpus, nonzero execution evidence and reproduction. A round trip can preserve the same error in both directions; include an independent oracle or control.

## Tools and limits

Use Hypothesis, fast-check, proptest, libFuzzer, AFL++, Atheris or Echidna as appropriate. A bounded campaign without crashes records the search performed, not an absence of defects.

## Bundled reference

Read the [Trail of Bits method](../../../cyber-audit/references/upstream/trailofbits/plugins/property-based-testing/skills/property-based-testing/SOURCE.md) when needed. The [provenance lock](../../../cyber-audit/references/upstream-lock.json) records the snapshot and licence. Adapt Claude-specific tools and workflows to the available environment. Reading this reference does not authorize running its scripts or invoking its agents.

## References

- [LLVM libFuzzer](https://llvm.org/docs/LibFuzzer.html): Coverage-guided fuzzing.
- [OSS-Fuzz](https://github.com/google/oss-fuzz): External tool reference.
- [Trail of Bits skills](https://github.com/trailofbits/skills): Snapshot recorded in upstream-lock.json.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

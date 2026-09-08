# Native code and memory

## Procedure

1. Trace lengths, sizes, signed conversions, offsets and allocation arithmetic from the input format. Compare the value checked with the value actually used.

2. Review lifetime, ownership, aliasing, pointer invalidation and error cleanup. For Rust, establish preconditions for unsafe code and FFI; the language alone does not settle safety.

3. Check synchronization, memory ordering, callbacks, asynchronous cancellation and shared resources. Reconstruct the timing required for a race before targeted reproduction.

4. Compare source and optimized binary: hardening, secret erasure, branches on sensitive values and compiler differences. A debug test does not describe release behavior.

5. Build a harness around the real API and run suitable sanitizers on synthetic inputs. Minimize crashes, verify reproducibility and search for variants sharing the cause.

## Required evidence

Provide the minimal input, compiler options, trace, memory violation or broken invariant, and reachability context. A crash does not automatically establish code execution.

## Tools and limits

Use ASan, UBSan, TSan or Miri where compatible, plus libFuzzer or AFL++. Compile unknown code in a disposable environment with limits on time, memory and output.

## Bundled reference

Read the [Trail of Bits method](../../../cyber-audit/references/upstream/trailofbits/plugins/zeroize-audit/skills/zeroize-audit/SOURCE.md) when needed. The [provenance lock](../../../cyber-audit/references/upstream-lock.json) records the snapshot and licence. Adapt Claude-specific tools and workflows to the available environment. Reading this reference does not authorize running its scripts or invoking its agents.

## References

- [LLVM libFuzzer](https://llvm.org/docs/LibFuzzer.html): Coverage-guided fuzzing.
- [OSS-Fuzz](https://github.com/google/oss-fuzz): External tool reference.
- [Trail of Bits skills](https://github.com/trailofbits/skills): Snapshot recorded in upstream-lock.json.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

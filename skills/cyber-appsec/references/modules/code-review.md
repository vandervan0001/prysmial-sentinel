# Security code review

## Procedure

1. Map inputs, sensitive operations and existing checks. Trace values through controllers, services, ORMs, jobs and adapters. Read the control module exports; searching a single predicate can miss related checks.

2. Review canonicalization, interpolation, serialization, file paths, process creation, server-side URLs, permissions and mutable state. Distinguish a sensitive call using a constant from user input reaching that call.

3. Check error paths: skipped initialization, permissive fallback, errors converted to empty values, negative caching, timeouts and retries. Reconstruct behavior after exceptions or interruption.

4. Find differences between neighboring endpoints and between synchronous and deferred operations. For an identified flaw, establish the cause and an exact instance before expanding the variant search. Keep a safe comparison case.

5. Propose a local fix that restores the invariant. For security diffs, also inspect the actual bundle build and paths excluded from compilation in that environment.

## Required evidence

Each finding needs an input → check → operation → impact path. Include a test that rules out a competing explanation and the locations of variants actually verified.

## Tools and limits

Combine text search, symbol navigation and data-flow analysis. Semgrep and CodeQL can help identify candidates. Compare an identified source copy before attributing a regression to the latest diff.

## Bundled reference

Read the [Trail of Bits method](../../../cyber-audit/references/upstream/trailofbits/plugins/variant-analysis/skills/variant-analysis/SOURCE.md) when needed. The [provenance lock](../../../cyber-audit/references/upstream-lock.json) records the snapshot and licence. Adapt Claude-specific tools and workflows to the available environment. Reading this reference does not authorize running its scripts or invoking its agents.

## References

- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/): 5.0.0.
- [MITRE CWE](https://cwe.mitre.org/): Verify each identifier.
- [Trail of Bits skills](https://github.com/trailofbits/skills): Snapshot recorded in upstream-lock.json.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

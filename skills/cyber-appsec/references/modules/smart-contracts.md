# Smart contracts and protocols

## Procedure

1. Reconstruct value flows and invariants for solvency, supply, shares, rounding and permissions. Compare the declared specification with behavior the protocol permits.

2. Review reentrancy, effect ordering, external calls, unchecked returns, approvals and unusual token behavior. Include hooks, transfer fees and rebasing where the protocol accepts those assets.

3. Check prices and oracles: freshness, units, decimals, liquidity, sequence and required market conditions. State the economic assumptions behind each simulation.

4. Review initialization, upgrades, storage layout, governance, pause controls and privileged keys. Compare deployed bytecode with source before reusing audit results.

5. Write property tests and scenarios on a local chain or isolated fork using fictitious assets. Minimize counterexamples and check the same invariant after correction.

## Required evidence

Provide the broken invariant, preconditions, minimal sequence, asset balance and version. Slither warnings remain candidates; simulated losses must be labeled as simulated.

## Tools and limits

Use Slither, Foundry, Echidna or Medusa according to language and chain. A `latest` documentation URL can point to a development version; match the compiler. Keep real transactions and user keys outside the test harness.

## Bundled reference

Read the [Trail of Bits method](../../../cyber-audit/references/upstream/trailofbits/plugins/property-based-testing/skills/property-based-testing/SOURCE.md) when needed. The [provenance lock](../../../cyber-audit/references/upstream-lock.json) records the snapshot and licence. Adapt Claude-specific tools and workflows to the available environment. Reading this reference does not authorize running its scripts or invoking its agents.

## References

- [Solidity security considerations](https://docs.soliditylang.org/en/latest/security-considerations.html): The latest URL may show a development version.
- [Trail of Bits skills](https://github.com/trailofbits/skills): Snapshot recorded in upstream-lock.json.
- [SLSA](https://slsa.dev/spec/v1.2/): 1.2; approved specification, source and build tracks.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

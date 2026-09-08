# Cryptography and PQC migration

## Procedure

1. Trace key generation, storage, use, rotation and destruction. Distinguish data keys, key wrapping, signatures and credentials. Check failure and recovery behavior.

2. Check AEAD use, nonce uniqueness, domain separation, RNGs, KDFs, signature verification and context binding. Test malformed formats and validation errors against known vectors.

3. For code that depends on secrets, examine compiler output, branches, memory access and erasure. A branch-free source loop does not prove constant-time behavior on the target platform.

4. Inventory asymmetric cryptography and data lifetimes for PQC preparation. Check the published standard, maintained implementation, protocol support and measured interoperability separately.

5. Evaluate migration or hybrid operation in a laboratory with size, latency, certificate and rollback budgets. Check errata for the selected primitives; avoid improvised cryptographic substitutions.

6. Use the [targeted verification cases](../crypto-agility.md) when this surface is present. Select cases for the actual architecture and record the observed limits.

## Required evidence

Provide the key and primitive inventory, expected property, vector or measurement, platform and limitations. No statistical signal in a sample does not prove the absence of a side channel.

## Tools and limits

Use Wycheproof, assembly analysis and dudect as needed. FIPS 203 defines ML-KEM; it does not certify the library or deployed protocol.

## Bundled reference

Read the [Trail of Bits method](../../../cyber-audit/references/upstream/trailofbits/plugins/constant-time-analysis/skills/constant-time-analysis/SOURCE.md) when needed. The [provenance lock](../../../cyber-audit/references/upstream-lock.json) records the snapshot and licence. Adapt Claude-specific tools and workflows to the available environment. Reading this reference does not authorize running its scripts or invoking its agents.

## References

- [NIST ML-KEM](https://csrc.nist.gov/pubs/fips/203/final): FIPS 203.
- [Project Wycheproof](https://github.com/C2SP/wycheproof): External test vector reference.
- [Trail of Bits skills](https://github.com/trailofbits/skills): Snapshot recorded in upstream-lock.json.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

# Cryptographic inventory and migration

Use this procedure when a project stores long-lived confidential data, signs artifacts or depends on cryptographic protocols that may need migration.

Inventory each use by asset, primitive, parameter set, implementation/version, provider, key owner, protocol, peer compatibility and expected lifetime. Include backups, firmware signing, authentication, certificates and recovery keys. An algorithm name in source does not prove which provider or parameters run in production.

FIPS 203 specifies ML-KEM for key encapsulation. FIPS 204 specifies ML-DSA and FIPS 205 specifies SLH-DSA for signatures. Keep these roles distinct; a KEM does not replace an authentication signature. Check each standard's errata and the implementation's validation status separately. [FIPS 203](https://csrc.nist.gov/pubs/fips/203/final), [FIPS 204](https://csrc.nist.gov/pubs/fips/204/final), [FIPS 205](https://csrc.nist.gov/pubs/fips/205/final).

| Property | Laboratory check |
|---|---|
| Correctness | Published vectors, malformed encodings, wrong key/context and independent verification |
| Context binding | Change protocol role, object type or signed metadata while retaining the signature |
| Failure behavior | Invalid ciphertext/signature follows the specified failure contract without leaking secrets |
| Interoperability | Actual client/server versions and negotiated parameters, including unsupported peers |
| Resource cost | Message size, handshake limits, storage, signing throughput and device constraints |
| Migration | Key rollover, verification of old artifacts, rollback policy and recovery after interruption |

For hybrid mechanisms, use a specified construction with maintained implementations. Do not concatenate algorithms or substitute a primitive into an existing protocol by analogy. Record which downgrade behavior is intentional and how peers authenticate negotiation.

Retest optimized binaries when implementation code handles secrets. Negative timing measurements on one CPU and compiler are bounded observations. [Wycheproof](https://github.com/C2SP/wycheproof) supplies adversarial vectors for supported algorithms; verify its actual coverage before selecting a suite.

Deliver a migration backlog tied to data lifetime and system dependencies. Distinguish inventory complete, prototype tested, interoperable deployment and independently validated cryptographic module. None of these alone establishes that an entire product is secure against future quantum attacks.

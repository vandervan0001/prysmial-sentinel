# Firmware, IoT and embedded devices

## Procedure

1. Hash the image and preserve the original. Extract in an isolated environment with file-count and size limits; inspect symlinks and archive paths before writing.

2. Inventory components, services, potential secrets and default configuration. Match discovered versions to the exact firmware and vendor backports.

3. Review the boot chain, update signatures, signer identity and rollback protection. A signature included in an archive does not prove the device checks it.

4. Review debug interfaces, provisioning, device identity, key storage and reset behavior. Distinguish physical-access attacks from exposed network inputs.

5. On an authorized emulator or laboratory device, test update formats, simulated power loss and restoration. Document limitations that prevent reproducing physical behavior.

6. Use the [targeted verification cases](../recovery-validation.md) when this surface is present. Select cases for the actual architecture and record the observed limits.

## Required evidence

Provide the hash, model, firmware, extraction path and observation. A string in a binary does not prove a service is active.

## Tools and limits

Use Binwalk, Ghidra, format tools and emulation as appropriate. Treat extractors and unknown firmware as untrusted code or input; run without host-system access.

## References

- [NIST OT security](https://csrc.nist.gov/pubs/sp/800/82/r3/final): 800-82 rev. 3.
- [OSS-Fuzz](https://github.com/google/oss-fuzz): External tool reference.
- [SLSA](https://slsa.dev/spec/v1.2/): 1.2; approved specification, source and build tracks.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

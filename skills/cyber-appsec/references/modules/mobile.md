# Mobile applications

## Procedure

1. Compare source and binary: build configuration, endpoints, debug flags, libraries and permissions. A vulnerable debug configuration may not describe the release.

2. Review local storage, Keychain/Keystore, backups, logs, screenshots and shared files. Assess sensitivity against the attacker model and device state.

3. Test deep links, intents, exported components, URL schemes, Universal/App Links and WebViews. Check origin, parameters and server authorization after navigation.

4. Check TLS trust, network configuration, authentication and account binding. Missing certificate pinning is not automatically a flaw without an applicable requirement.

5. Test lifecycle changes, logout, background execution, revocation and account switching. Verify that data or jobs from the previous session do not persist beyond policy.

## Required evidence

Identify the versioned MASVS requirement, relevant MASTG test, binary version and device. Distinguish static analysis, stock devices and modified devices.

## Tools and limits

Use MobSF, JADX, Android/Apple tools and Frida instrumentation in an authorized laboratory. Exploitation on a modified device does not establish the same result on a stock user device.

## References

- [OWASP MASVS and MASTG](https://mas.owasp.org/): Select versioned requirements and tests.
- [NIST Digital Identity Guidelines](https://csrc.nist.gov/pubs/sp/800/63/4/final): 800-63-4, July 2025.
- [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x11-t10/): 2023.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

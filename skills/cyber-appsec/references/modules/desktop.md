# Desktop, Electron and extensions

## Procedure

1. Trace remote content and renderer access to the privileged process. For Electron, check context isolation, sandboxing, Node integration and the actual preload API.

2. Review each IPC method: sender, frame, origin, parameter schema, authorized object and system action. Exposing the entire transport through a bridge broadens access.

3. Check URL opening, navigation, protocol handlers, imported files and document rendering. Validate destinations after canonicalization and prevent user-controlled paths from becoming commands.

4. Review updates, signatures, rollback and artifact origins. Verify that the expected identity is checked before installation; a signature merely being present is insufficient.

5. For extensions, trace host permissions, content scripts, service workers and native messaging. Check each message sender, cross-origin access, token storage and capture shutdown after logout.

## Required evidence

Provide the untrusted content → bridge → privileged action chain and identify the affected binary. Verify behavior in the shipped runtime, including native dependency ABI.

## Tools and limits

Use DevTools, package inspection and local IPC tests. Do not disable runtime protections to make a test pass. Tauri capabilities and extension permissions depend on version.

## References

- [Electron security](https://www.electronjs.org/docs/latest/tutorial/security): Match the bundled Electron version.
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/): 5.0.0.
- [NIST Digital Identity Guidelines](https://csrc.nist.gov/pubs/sp/800/63/4/final): 800-63-4, July 2025.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

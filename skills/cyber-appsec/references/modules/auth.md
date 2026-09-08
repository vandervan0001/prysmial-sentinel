# Authentication and authorization

## Procedure

1. Reconstruct registration, verification, sign-in, recovery, account linking and authentication factor changes. Look for recovery paths weaker than the main authentication flow.

2. Check sessions and revocation across cookies, APIs, WebSocket connections and jobs. Test account disablement, logout and refresh-token rotation alongside a still-valid session.

3. For OAuth/OIDC, check issuer, audience, exact redirect URI, state, flow-specific nonce requirements, PKCE, session binding and privileges. Read the provider guidance and RFC 9700 for the actual client type.

4. For WebAuthn and passkeys, examine RP ID, origin, single-use challenge, account binding and user verification requirements for the action. Include enrollment and recovery in the review.

5. Build a subject × action × object matrix covering direct access, lists, exports, search, attachments, admin operations and deferred jobs. A permission check in the interface does not protect the server function.

## Required evidence

Run an authorized operation, then repeat the path with a forbidden account or object. Record role, object, session state and persistent effect, with secrets masked.

## Tools and limits

Use an HTTP proxy and server tests with synthetic accounts. Unpredictable identifiers do not replace authorization. Match NIST assurance requirements to the service; this review does not establish compliance by itself.

## References

- [NIST Digital Identity Guidelines](https://csrc.nist.gov/pubs/sp/800/63/4/final): 800-63-4, July 2025.
- [OAuth Security BCP](https://www.rfc-editor.org/rfc/rfc9700.html): RFC 9700, January 2025.
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/): 5.0.0.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

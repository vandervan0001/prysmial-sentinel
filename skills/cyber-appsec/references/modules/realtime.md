# WebSocket, SSE and message queues

## Procedure

1. Check the handshake and authorization of each subscription and message. Bind channels to server objects; resolve any client-supplied tenant against the authorized identity.

2. Test expiry, logout, role removal, closure and reconnection. Reassess channels opened before revocation according to the declared policy.

3. Check WebSocket Origin and transport-appropriate CSRF protection. CORS alone does not control the WebSocket handshake. For SSE, review cookies, caching and Last-Event-ID recovery.

4. Test ordering, duplication, replay, recovery, dead-letter handling and partial state with synthetic messages. Broker guarantees do not create a transaction with the business database.

5. Review limits per message, queue, connection and identity, plus backpressure and cancellation. Verify that limits stop the actual processing. Hiding client-side output does not enforce a processing limit.

## Required evidence

Show two subscribers with distinct identities and channels, then a known event received only by the authorized subject. For a leak, retain the observed routing with synthetic content.

## Tools and limits

Use local protocol clients and sanitized broker traces. Set connection, volume and time limits. Saturation tests against a live service require explicit scope.

## References

- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/): Read the relevant guide.
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/): 5.0.0.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

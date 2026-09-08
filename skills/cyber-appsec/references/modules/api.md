# APIs and data isolation

## Procedure

1. Compare the route inventory, schemas and active handlers. Include internal endpoints exposed through proxies, older API versions, GraphQL mutations and gRPC methods.

2. Test access to objects and properties: reads, partial updates, mass assignment, list filters and aggregates. Find paths that omit a restriction applied in the main CRUD handler.

3. For GraphQL, review cost, depth, aliases, batching, subscriptions and resolver authorization. Introspection alone is not a vulnerability.

4. Trace user-supplied URLs through DNS, redirects and server requests. Test destination and outbound restrictions in a laboratory with a controlled receiver; do not contact real cloud metadata services by default.

5. Check webhook validation against raw bytes, signatures, timestamps, replay, idempotency and the associated business object. For uploads, examine actual file type, names, archive extraction, size, storage and download paths.

6. Use the [targeted verification cases](../parser-boundaries.md) when this surface is present. Select cases for the actual architecture and record the observed limits.

## Required evidence

Keep the minimal sanitized request, identity, object, response and effect. A 200 response with no objects can hide incorrectly combined filters; check against a known existing object.

## Tools and limits

Use ZAP, Burp or contract tests within the authorized scope. OpenAPI-generated tests can find contract mismatches, but do not establish business rules or permissions.

## References

- [OWASP API Security Top 10](https://owasp.org/API-Security/editions/2023/en/0x11-t10/): 2023.
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/): 5.0.0.
- [OWASP WSTG](https://owasp.org/www-project-web-security-testing-guide/): Check the stable version when starting the review.
- [PostgreSQL row security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html): Match the role and database version.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

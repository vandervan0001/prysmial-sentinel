# Business logic and concurrency

## Procedure

1. Map the state machine and separate server transitions, provider callbacks and interface behavior. Look for skipped steps, role changes during an operation and actions after cancellation.

2. Check idempotency and binding between the key, subject, operation and parameters. The cache must distinguish repeated identical requests from different requests.

3. Use synthetic data and a controlled order of concurrent requests to expose the window between checking and writing. Check transactions, uniqueness constraints, isolation and recovery after conflicts.

4. For money or quantities, trace rounding, currency, quantity, sign, decimals, limits and price sources. Compare invariants before and after the operation, including compensation, without real billing.

5. Review distributed quotas, reservations, expiry and job recovery. A retry after a timeout may repeat an operation already completed by a third party.

## Required evidence

Demonstrate the broken invariant with initial state, operation order and final state. Include the same scenario run sequentially as a control. A burst of requests alone does not prove a race condition.

## Tools and limits

Use transaction tests and controlled barriers with bounded load. For payment tests, verify that the provider configuration uses test mode.

## References

- [OWASP WSTG](https://owasp.org/www-project-web-security-testing-guide/): Check the stable version when starting the review.
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/): 5.0.0.
- [Trail of Bits skills](https://github.com/trailofbits/skills): Snapshot recorded in upstream-lock.json.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

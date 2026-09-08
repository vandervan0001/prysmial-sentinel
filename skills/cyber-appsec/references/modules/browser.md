# Browser and frontend security

## Procedure

1. Trace untrusted data into DOM sinks, templates, URLs, styles and Markdown rendering. Check sanitization in the final context, including later transformations.

2. Read response headers on actual routes, including errors and cache hits. Assess CSP against dynamically loaded scripts; use report-only mode when a proposed change could break application flows.

3. Relate CORS to the credential model. Test expected, unexpected and null origins as applicable. A permissive header without sensitive data or credentials is insufficient to establish impact.

4. Test CSRF on cookie-authenticated mutations, forms and method or content-type changes. Check Origin, tokens and SameSite behavior on the exposed flow.

5. Review postMessage, window.opener, iframes, service workers, CDN caches and browser storage. Verify that authenticated responses cannot be reused by another identity.

## Required evidence

Provide the origin, credentials used and affected action or data. Verify the path in a real browser. Do not report HTML injection without a JavaScript effect as confirmed XSS.

## Tools and limits

Use DevTools and a proxy with controlled captures. Verify document visibility, stylesheet loading and session state before measuring behavior. COOP, COEP and CORP depend on isolation needs and integrations.

## References

- [OWASP WSTG](https://owasp.org/www-project-web-security-testing-guide/): Check the stable version when starting the review.
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/): 5.0.0.
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/): Read the relevant guide.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

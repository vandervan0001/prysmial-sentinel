# Sensitive data and isolation

## Procedure

1. Map collection, storage, indexes, logs, analytics, exports, prompts and backups. Compare documented data flows with data actually sent.

2. Look for excessive fields, identifiers in URLs, request logging and overly broad responses. Check redaction before transfer or storage, including paths outside the interface.

3. Review access to primary and derived data: search, attachments, reports, caches, backups and support access.

4. Test retention and deletion with a synthetic identifier traced through every known copy. Document delays, backup exceptions and deferred effects.

5. Assess exports to third-party services and models: content, configured region, retention and available controls. Record technical verification separately from any legal assessment.

## Required evidence

Provide the data-flow map, fields, authorized identities, exposure paths and deletion evidence for each storage location. A written policy does not establish enforcement.

## Tools and limits

Use laboratory network traces and bounded queries on synthetic data. This technical review alone cannot establish GDPR or Swiss FADP compliance.

## References

- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/): 5.0.0.
- [OWASP GenAI LLM Top 10](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/): 2026, August 2026.
- [PostgreSQL row security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html): Match the role and database version.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

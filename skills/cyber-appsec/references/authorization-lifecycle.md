# Authorization across time and storage

Use this procedure when an application has accounts, shared workspaces, background jobs, caches or delegated access. First establish its actual sharing model. A company field alone does not establish a tenant boundary.

## Build the test matrix

Create two authorized synthetic identities with distinguishable records. For each path below, identify the principal used at the point of access, the permission decision and the final data sink.

| Path | Counterexample to try locally | Evidence of the intended behavior |
|---|---|---|
| Detail, list, count, export, attachment | Change only the object or owner identifier | Permitted object is present; forbidden object is withheld |
| Shared cache | Prime as A, then repeat as B; reverse the order | Cache entries and invalidation follow the actual visibility policy |
| Queue or scheduled job | Revoke access between enqueue and execution | Execution follows the documented revocation policy and records the acting identity |
| Search, embeddings, reranking | Use a query that matches a forbidden record | Retrieval and returned citations respect access before content reaches the model |
| WebSocket or SSE | Revoke access with a subscription already open | Existing streams stop disclosing data within the defined revocation interval |
| Approval or signed action | Change destination, parameters or identity after approval | The invoked action still matches what was authorized |
| Retry | Repeat an operation after an ambiguous timeout | Persistent effect follows the defined idempotency contract |

Include support and administrative roles, service identities, deleted users, account switching and grants that expire. Distinguish intentional delegation from an operation that silently inherits the worker's broad privileges.

## Database and transaction boundaries

When PostgreSQL RLS is part of the design, test with the real application role. Superusers and `BYPASSRLS` roles bypass row policies; owners normally do too. Inspect `USING`, `WITH CHECK`, applicable roles and policy combinations. Check functions, views and jobs that run under a different identity. A passing test under the wrong role cannot establish application isolation. [PostgreSQL row security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html).

For connection pools, check where identity context is set, its transaction lifetime and cleanup after errors. Test alternating identities on a reused connection. For concurrent changes, use barriers around the real check and write; retain initial state, operation order and final state.

## Acceptance

Require an allowed operation that succeeds and a prohibited operation that reaches the same processing path before denial. Inspect persisted state and emitted jobs, not only the response code. Re-run the pair after a correction and search other consumers of the same authorization or cache helper.

These are Sentinel test designs informed by [ASVS](https://owasp.org/www-project-application-security-verification-standard/) and [OWASP API Security](https://owasp.org/API-Security/editions/2023/en/0x11-t10/). They are not a claim of complete ASVS coverage.

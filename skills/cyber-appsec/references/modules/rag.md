# RAG, search and memory

## Procedure

1. Trace document → chunking → embedding → index → filter → reranker → context → response. Check where identity and ACLs are enforced, including ingestion and updates.

2. Create two corpora with distinct markers. Verify that a query finds an authorized document, then repeat the query with a forbidden identity. An empty search without a positive control does not test the ACL.

3. Review caches, conversation history, shared memory, exports and citations for leaks between users. Check that cache keys include all required authorization context.

4. Test updates, access revocation and deletion through indexes and caches. Verify both source document removal and removal of derived copies.

5. For poisoning tests, use laboratory documents with instructions unrelated to the task. Observe selection, provenance and influence on tools without inserting the test corpus into a live index.

6. Use the [targeted verification cases](../authorization-lifecycle.md) when this surface is present. Select cases for the actual architecture and record the observed limits.

## Required evidence

Keep synthetic IDs, expected ACLs, intermediate results and the context sent to the model. A response can omit the marker even if the model received a forbidden document; inspect access before generation.

## Tools and limits

Use read-only queries, fixtures and sanitized traces. Search quality and confidentiality require separate measurements and a relevant control for each.

## References

- [OWASP GenAI LLM Top 10](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/): 2026, August 2026.
- [Agent Security Bench paper](https://arxiv.org/abs/2410.02644): 2024, ICLR 2025.
- [AgentSecBench](https://arxiv.org/abs/2605.26269): 2026 preprint.
- [PostgreSQL row security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html): Match the role and database version.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

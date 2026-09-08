# Literature review: 8 September 2026

This review selected primary sources that could change Sentinel's audit decisions: current standards and protocol guidance, implementation documentation, and research with an inspectable evaluation method. It is a targeted review, not an exhaustive survey of security literature. The registry contains 59 references; link availability is recorded separately from substantive review.

## Standards and implementation guidance

| Source and reviewed material | Decision in Sentinel | Scope of the evidence |
|---|---|---|
| [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/), stable release and requirement naming | Retain 5.0.0 and versioned identifiers | Release status and naming verified; no claim that all ASVS requirements were mapped |
| [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html), OAuth security guidance | Keep flow-specific issuer, audience, redirect and session checks | Apply to the actual client and provider; deployment is not verified by the RFC |
| [MCP security guidance, 2026-07-28](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices), authorization, discovery and state boundaries | Extend tests for discovery destinations, state ownership, minimal scopes and client metadata | Versioned guidance reviewed; implementations remain project-specific |
| [SLSA 1.2](https://slsa.dev/spec/v1.2/) and [artifact verification](https://slsa.dev/spec/v1.2/verifying-artifacts) | Replace 1.1 links; verify subject digest, expected builder, source and parameters | Approved specification; Sentinel does not claim a SLSA level |
| [NIST SSDF publications](https://csrc.nist.gov/Projects/ssdf/publications) and [GenAI profile](https://csrc.nist.gov/pubs/sp/800/218/a/final) | Separate final SSDF 1.1, draft 1.2 and the published AI profile | Publication records reviewed; no clause-level conformity assessment |
| [PostgreSQL RLS](https://www.postgresql.org/docs/current/ddl-rowsecurity.html), role bypass and policy behavior | Test actual application roles and alternate access paths | PostgreSQL 18 page reviewed; match the deployed version |
| [OWASP SSRF prevention](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html) and [RFC 9112](https://www.rfc-editor.org/rfc/rfc9112.html), framing and smuggling | Add controlled URL-resolution and parser-chain cases | Behavior must be measured across the actual parsers and network policy |
| [FIPS 204](https://csrc.nist.gov/pubs/fips/204/final) and [FIPS 205](https://csrc.nist.gov/pubs/fips/205/final), algorithm roles and publication notices | Add ML-DSA and SLH-DSA alongside ML-KEM; require errata review | Publication records reviewed; cryptographic proofs and implementations were not revalidated |
| [Sigma specification](https://sigmahq.io/sigma-specification/) | Separate rule, conversion, collection and correlation checks | Specification entry point reviewed; actual backend semantics require tests |
| [NIST SP 800-82 rev. 3](https://csrc.nist.gov/pubs/sp/800/82/r3/final) and [SP 800-61 rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) | Preserve OT operating constraints and separate containment from recovery verification | Published baselines confirmed; no live device test or compliance claim |

## Agent research and new OWASP resources

| Source and inspected material | Retained lesson | Limit carried into the methods |
|---|---|---|
| [AgentDojo v3](https://arxiv.org/html/2406.13352v3), environment-state checks and security/utility evaluation | Measure task completion and prohibited effects independently | Its tasks and tested models do not establish Sentinel's detection rate |
| [Firewall benchmark analysis v2](https://arxiv.org/html/2510.05244v2), benchmark critique and evaluation design | Check metrics, setup failures and stronger held-out scenarios before interpreting an all-pass result | Published benchmark saturation is not a guarantee against untested attacks |
| [AgentSecBench v1](https://arxiv.org/html/2605.26269v1), security properties, paired controls and section 10 limitations | Separate instruction integrity, confidentiality and action integrity | Exact markers miss semantic variants; small deterministic models and lexical utility measures limit transfer |
| [Runtime Skill Audit v1](https://arxiv.org/html/2606.11671v1), runtime method and section 7 limitations | Exercise skills with relevant local context and inspect effects | The 100-skill OpenClaw study is non-exhaustive and uses model-dependent judgments |
| [OWASP LLM Top 10 2026](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/), release page | Retain the August 2026 risk reference | A risk list does not specify a complete product test suite |
| [ACS](https://genai.owasp.org/resource/agent-control-standard-acs/) and its [repository overview](https://github.com/GenAI-Security-Project/agent-control-standard) | Test the middleware hooks actually traversed by actions, including failure paths | Resource published 1 September 2026; no implementation or interoperability certification |
| [OWASP GenAI framework crosswalk](https://genai.owasp.org/resource/genai-security-industry-framework-crosswalk/), resource overview | Use mappings to locate requirements, then verify wording and applicability | Resource published 1 September 2026; mappings were not imported as automatic coverage claims |

The research experiments above were not reproduced. Sentinel's [independent synthetic review](examples/review-lab-report.md) is a separate, smaller evaluation. It does not inherit their datasets, results or validation claims.

## Original analysis and resulting changes

The seven targeted guides convert the reviewed concepts and repository analysis into cases for authorization lifetime, parsers, agents, supply chains, cryptographic migration, telemetry and OT recovery. These are Sentinel test designs, with their supporting references identified. They are not presented as verbatim standard requirements or as novel research.

Reviewing Sentinel itself reproduced three reporting defects: redaction merged distinct finding locations, Windows paths were treated as remote URLs, and candidate reports accepted promoted statuses. Regression tests cover their corrections. The runner now rejects project-supplied scanner paths and bounds output as well as runtime. Tests also exposed mutable observations in the example harness; collected results now preserve a copy of the state at observation time.

Future source updates should record what was read, its version, the supported claim, the resulting check and unresolved limits. A working URL, a GitHub star count or a model-generated explanation alone does not establish that a method works.

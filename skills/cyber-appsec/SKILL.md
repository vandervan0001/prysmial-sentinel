---
name: cyber-appsec
description: "Review code, APIs, identity, cloud, CI/CD, AI applications, mobile, desktop and native components using methods selected for the project."
---

# AppSec, cloud and AI

Review code, APIs, identity, cloud, CI/CD, AI applications, mobile, desktop and native components using methods selected for the project.

Read the [shared contract](../cyber-audit/references/engagement.md). Start from the available evidence and permissions already established in the session. Load the method that addresses the question.

## Methods

| Method | Use |
|---|---|
| [Security code review](references/modules/code-review.md) | Review code and diffs for security defects, then trace related variants across the project. |
| [Static analysis and rules](references/modules/sast.md) | Configure Semgrep, CodeQL and SARIF analysis for the actual language, framework and tool edition. |
| [Dependencies and software supply chain](references/modules/dependencies.md) | Review resolved dependencies, SBOMs, vulnerability advisories and component provenance. |
| [Secrets and credentials](references/modules/secrets.md) | Find exposed secrets and review their storage, distribution, rotation and removal. |
| [Authentication and authorization](references/modules/auth.md) | Review sign-in, sessions, OAuth/OIDC, passkeys and access to objects and functions. |
| [APIs and data isolation](references/modules/api.md) | Review REST, GraphQL, gRPC, webhooks, uploads and data isolation between users. |
| [Browser and frontend security](references/modules/browser.md) | Review XSS, CSP, CORS, CSRF, caches and browser trust boundaries in web applications. |
| [Business logic and concurrency](references/modules/business-logic.md) | Find workflow abuse, replay, race conditions and inconsistencies in billing or quotas. |
| [WebSocket, SSE and message queues](references/modules/realtime.md) | Review persistent connections, subscriptions, task queues and isolation between channels. |
| [Cloud and service identities](references/modules/cloud.md) | Review AWS, Azure, GCP or application cloud configuration and effective identity permissions. |
| [Kubernetes and orchestration](references/modules/kubernetes.md) | Review Kubernetes RBAC, admission, networking, secrets and workload isolation. |
| [Images and containers](references/modules/containers.md) | Review OCI images, Dockerfiles, layers, privileges and runtime configuration. |
| [Infrastructure as code](references/modules/iac.md) | Review Terraform, OpenTofu, CloudFormation, Helm and infrastructure policies before deployment. |
| [CI/CD and development agents](references/modules/cicd.md) | Review pipelines, runners, releases, provenance and AI agent integrations in software delivery. |
| [LLMs and AI agents](references/modules/ai.md) | Review LLM applications and agents for prompt injection, excessive permissions, data leaks and tool abuse. |
| [MCP, skills and connectors](references/modules/mcp.md) | Review MCP servers and clients, imported skills and connectors that give agents access to tools or data. |
| [RAG, search and memory](references/modules/rag.md) | Review ingestion, vector search, reranking, citations and persistent memory in AI systems. |
| [Mobile applications](references/modules/mobile.md) | Review Android and iOS applications using MASVS/MASTG, source code and the distributed binary. |
| [Desktop, Electron and extensions](references/modules/desktop.md) | Review privilege boundaries in Electron, Tauri, desktop applications and browser extensions. |
| [Native code and memory](references/modules/native.md) | Review C, C++, Rust, FFI and binary processing for memory corruption and concurrency defects. |
| [Fuzzing and property tests](references/modules/fuzzing.md) | Build fuzzing campaigns and property tests for parsers, protocols and state transitions. |
| [Cryptography and PQC migration](references/modules/crypto.md) | Review cryptography use, key management, sensitive implementations and post-quantum migration readiness. |
| [Smart contracts and protocols](references/modules/smart-contracts.md) | Review blockchain contracts and protocols using code, invariants and local-chain tests. |
| [Sensitive data and isolation](references/modules/privacy.md) | Review sensitive data flows, minimization, access, retention and deletion. |
| [Remediation and retesting](references/modules/remediation.md) | Fix a confirmed security defect and verify the correction, legitimate behavior and related variants. |

Read the [domain guide](references/domain.md) for tool selection and handoffs. Bundled third-party references do not authorize tool execution.

Report findings with the [evidence template](../cyber-audit/references/finding-template.md), separating verified coverage, hypotheses and untested checks.

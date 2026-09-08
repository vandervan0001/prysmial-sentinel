# Domain and method catalogue

The audit coordinator selects from eight domain skills. Each domain loads its specialist methods as needed.

## Cyber references and evidence

Entry point: [cyber-core](skills/cyber-core/SKILL.md).

Connect observations to ATT&CK techniques, requirements, evidence and priorities when planning or reporting a security review.

| Method | Use |
|---|---|
| [Threat modeling](skills/cyber-core/references/modules/threat-model.md) | Model threats for an architecture, service or planned change before the security review. |
| [Finding triage and reporting](skills/cyber-core/references/modules/triage.md) | Verify scanner findings, reject false positives and write an evidence-based security report. |
| [Security research](skills/cyber-core/references/modules/research.md) | Find current vendor advisories, standards, research and tools for a specific security question. |

## Pentesting and exposure

Entry point: [cyber-pentest](skills/cyber-pentest/SKILL.md).

Review attack surface and run authorized application, network, Windows/AD and Linux tests with minimal evidence.

| Method | Use |
|---|---|
| [Networks, DNS and TLS](skills/cyber-pentest/references/modules/network.md) | Review network exposure, TLS, DNS, proxies and segmentation from configuration or authorized targets. |
| [Application pentesting](skills/cyber-pentest/references/modules/pentest.md) | Plan and run scoped application tests with bounded active checks and minimal evidence. |
| [Windows, AD and Entra](skills/cyber-pentest/references/modules/windows-ad.md) | Review Windows, Active Directory and Entra identities using exports and privilege paths. |
| [Linux and system services](skills/cyber-pentest/references/modules/linux.md) | Review Linux configuration, services, local privileges and server or container isolation. |

## AppSec, cloud and AI

Entry point: [cyber-appsec](skills/cyber-appsec/SKILL.md).

Review code, APIs, identity, cloud, CI/CD, AI applications, mobile, desktop and native components using methods selected for the project.

| Method | Use |
|---|---|
| [Security code review](skills/cyber-appsec/references/modules/code-review.md) | Review code and diffs for security defects, then trace related variants across the project. |
| [Static analysis and rules](skills/cyber-appsec/references/modules/sast.md) | Configure Semgrep, CodeQL and SARIF analysis for the actual language, framework and tool edition. |
| [Dependencies and software supply chain](skills/cyber-appsec/references/modules/dependencies.md) | Review resolved dependencies, SBOMs, vulnerability advisories and component provenance. |
| [Secrets and credentials](skills/cyber-appsec/references/modules/secrets.md) | Find exposed secrets and review their storage, distribution, rotation and removal. |
| [Authentication and authorization](skills/cyber-appsec/references/modules/auth.md) | Review sign-in, sessions, OAuth/OIDC, passkeys and access to objects and functions. |
| [APIs and data isolation](skills/cyber-appsec/references/modules/api.md) | Review REST, GraphQL, gRPC, webhooks, uploads and data isolation between users. |
| [Browser and frontend security](skills/cyber-appsec/references/modules/browser.md) | Review XSS, CSP, CORS, CSRF, caches and browser trust boundaries in web applications. |
| [Business logic and concurrency](skills/cyber-appsec/references/modules/business-logic.md) | Find workflow abuse, replay, race conditions and inconsistencies in billing or quotas. |
| [WebSocket, SSE and message queues](skills/cyber-appsec/references/modules/realtime.md) | Review persistent connections, subscriptions, task queues and isolation between channels. |
| [Cloud and service identities](skills/cyber-appsec/references/modules/cloud.md) | Review AWS, Azure, GCP or application cloud configuration and effective identity permissions. |
| [Kubernetes and orchestration](skills/cyber-appsec/references/modules/kubernetes.md) | Review Kubernetes RBAC, admission, networking, secrets and workload isolation. |
| [Images and containers](skills/cyber-appsec/references/modules/containers.md) | Review OCI images, Dockerfiles, layers, privileges and runtime configuration. |
| [Infrastructure as code](skills/cyber-appsec/references/modules/iac.md) | Review Terraform, OpenTofu, CloudFormation, Helm and infrastructure policies before deployment. |
| [CI/CD and development agents](skills/cyber-appsec/references/modules/cicd.md) | Review pipelines, runners, releases, provenance and AI agent integrations in software delivery. |
| [LLMs and AI agents](skills/cyber-appsec/references/modules/ai.md) | Review LLM applications and agents for prompt injection, excessive permissions, data leaks and tool abuse. |
| [MCP, skills and connectors](skills/cyber-appsec/references/modules/mcp.md) | Review MCP servers and clients, imported skills and connectors that give agents access to tools or data. |
| [RAG, search and memory](skills/cyber-appsec/references/modules/rag.md) | Review ingestion, vector search, reranking, citations and persistent memory in AI systems. |
| [Mobile applications](skills/cyber-appsec/references/modules/mobile.md) | Review Android and iOS applications using MASVS/MASTG, source code and the distributed binary. |
| [Desktop, Electron and extensions](skills/cyber-appsec/references/modules/desktop.md) | Review privilege boundaries in Electron, Tauri, desktop applications and browser extensions. |
| [Native code and memory](skills/cyber-appsec/references/modules/native.md) | Review C, C++, Rust, FFI and binary processing for memory corruption and concurrency defects. |
| [Fuzzing and property tests](skills/cyber-appsec/references/modules/fuzzing.md) | Build fuzzing campaigns and property tests for parsers, protocols and state transitions. |
| [Cryptography and PQC migration](skills/cyber-appsec/references/modules/crypto.md) | Review cryptography use, key management, sensitive implementations and post-quantum migration readiness. |
| [Smart contracts and protocols](skills/cyber-appsec/references/modules/smart-contracts.md) | Review blockchain contracts and protocols using code, invariants and local-chain tests. |
| [Sensitive data and isolation](skills/cyber-appsec/references/modules/privacy.md) | Review sensitive data flows, minimization, access, retention and deletion. |
| [Remediation and retesting](skills/cyber-appsec/references/modules/remediation.md) | Fix a confirmed security defect and verify the correction, legitimate behavior and related variants. |

## Detection engineering

Entry point: [cyber-detection](skills/cyber-detection/SKILL.md).

Write and verify Sigma, YARA and SIEM detections against defined telemetry, with positive and benign test cases.

| Method | Use |
|---|---|
| [Detection and telemetry](skills/cyber-detection/references/modules/detection.md) | Review detection coverage and write Sigma, YARA or network rules using laboratory traces. |

## Threat hunting

Entry point: [cyber-hunting](skills/cyber-hunting/SKILL.md).

Investigate a hypothesis using logs and ATT&CK behaviors, then assess findings and collection gaps.

[Domain guide](skills/cyber-hunting/references/domain.md).

## Detection validation

Entry point: [cyber-purple-team](skills/cyber-purple-team/SKILL.md).

Validate behavior, telemetry, detection and alert delivery in an authorized laboratory using reviewed Atomic scenarios.

[Domain guide](skills/cyber-purple-team/references/domain.md).

## Investigation and response

Entry point: [cyber-dfir](skills/cyber-dfir/SKILL.md).

Collect and analyze digital evidence, assess an incident or suspicious artifact, and prepare containment and recovery.

| Method | Use |
|---|---|
| [Incident response and evidence](skills/cyber-dfir/references/modules/incident.md) | Analyze an incident, build a timeline and prepare containment, recovery and verification. |

## Industrial OT and ICS security

Entry point: [cyber-ot](skills/cyber-ot/SKILL.md).

Review OT/ICS architecture, captures and exports using protocol, firmware, vendor and IEC 62443 methods.

| Method | Use |
|---|---|
| [OT, ICS and control systems](skills/cyber-ot/references/modules/ot.md) | Review industrial architecture, controllers, supervision and maintenance access from documents or laboratory evidence. |
| [Firmware, IoT and embedded devices](skills/cyber-ot/references/modules/firmware.md) | Review firmware and IoT devices using supplied images, source code and laboratory interfaces. |

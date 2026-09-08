# Selecting AppSec methods

AppSec covers code, delivery configuration and application identities. Active tests described in its methods remain subject to the session scope.

| Project context | Methods to load |
|---|---|
| Web application or SaaS | Authentication, APIs, browser, business logic, dependencies and secrets |
| AI with tools | AI, MCP, RAG, authentication and APIs according to the data flows |
| Cloud or Kubernetes | Cloud, IaC, Kubernetes, containers and CI/CD |
| Mobile or desktop | Platform, authentication, APIs and update provenance |
| Native code or cryptography | Native code, fuzzing, cryptography and secrets |
| Contracts and value flows | Smart contracts, property tests and privileged roles |
| Confirmed issue to fix | Code review, variant analysis, remediation and retesting |

Open the method from the table in `SKILL.md`. Add methods when the architecture supports them. A `package.json` file alone does not justify every web and AI check.

The six bundled rules are a tested starting set. Official Semgrep, Trail of Bits and elttam collections remain references to select and version. Their licences differ: the registry records the Semgrep Rules License for Semgrep, declared AGPL-3.0 for Trail of Bits and MIT for elttam. No complete rule pack is redistributed or run by default.

For imported rules, retain identifier, source, commit, licence, engine compatibility and fixtures. Test safe and vulnerable cases relevant to the framework before adding a rule to CI. Rules intended to inventory behavior must not automatically produce confirmed vulnerabilities.

For software delivery, trace commit, build, image, publishing identity and running artifact. Check signatures and SBOMs against these identified objects. An attestation from a builder whose output an attacker can control does not establish the claimed property.

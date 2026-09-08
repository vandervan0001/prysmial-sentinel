# Agent authority and evaluation

Use this procedure when retrieved content, MCP, skills, tools or persistent memory can affect an action. Record the application policy before asking a model to interpret the test.

## Trace the authority path

Map user intent → retrieved data → proposed call → authorization → execution → persistent effect. At each boundary, identify which component enforces identity, object access, destination, permitted operation and budget. State whether that component sees the same values that execution uses.

Create paired tests using synthetic markers and an in-memory effect sink:

| Boundary | Adversarial variation | Benign control |
|---|---|---|
| Retrieved page, attachment, OCR or tool response | Content asks for an unrelated action or disclosure | The same task with relevant ordinary content |
| Tool definition or skill | Description or referenced resource changes the proposed destination | Reviewed tool performs the originally requested operation |
| Approval | Action changes after approval, is replayed, or changes identity | Exact authorized action executes according to its repeat policy |
| Memory | A stored instruction influences a later task or another user | Legitimate retained preference remains usable |
| Delegation | A helper receives broader scope than its caller | Required narrow capability still works |
| Failure and retry | Timeout occurs after a simulated persistent effect | A safe retry completes without an unintended second effect |

A refusal in assistant text is one observation. Record actual tool arguments, blocked calls, reads, outbound attempts and persistent effects independently. Exact-marker tests do not measure every semantic disclosure channel.

## MCP-specific review

Match the negotiated protocol and transport. For remote authorization, inspect issuer/resource binding, audience, per-client consent and minimal scopes. Evaluate discovery fetches, redirects and Client ID Metadata Documents against the deployment's destination policy. Check state handles and asynchronous results against the authenticated owner. Local stdio servers inherit OS privileges; a read-only annotation cannot restrict a process. [MCP security guidance, 2026-07-28](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices).

## Measure useful protection

If the application implements middleware such as [ACS](https://genai.owasp.org/resource/agent-control-standard-acs/), identify the hooks that actually wrap each execution path. Test a policy denial, a hook failure and an asynchronous or delegated call. Record whether a failed enforcement component blocks the action or permits it. An integration badge does not establish that every tool path passes through the middleware.

Record model identifier, harness and dataset revision, prompt version, tool policy, trials, budget and completion criteria. Report prohibited effects and legitimate task completion separately, with numerator and denominator. Preserve failed setup and invalid trials instead of dropping them from the denominator without explanation. Repeat stochastic trials and state the uncertainty; a small all-pass sample does not establish a universal success rate.

Keep holdout scenarios outside the tuning loop. Evaluate changed tools, retrieval formats and model versions again. Test an intentionally disabled enforcement component in a disposable copy to establish whether the evaluator can observe a violation.

These test designs draw on [AgentDojo](https://arxiv.org/abs/2406.13352), the [firewall benchmark analysis](https://arxiv.org/abs/2510.05244), [AgentSecBench](https://arxiv.org/abs/2605.26269) and [Runtime Skill Audit](https://arxiv.org/abs/2606.11671). Sentinel has not reproduced those published experiments. Its local fixture and independent review have the narrower scope recorded in [VALIDATION.md](../../../VALIDATION.md).

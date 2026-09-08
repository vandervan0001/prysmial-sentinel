# LLMs and AI agents

## Procedure

1. Separate trusted instructions from external data: pages, attachments, images, OCR, tool results and memory. Trace their influence on action parameters and responses.

2. Write scenarios with synthetic markers and simulated tools: changed destinations, unrequested actions, access to a forbidden document, replay and persistence in memory. Measure the effect; a refusal message alone is insufficient.

3. Examine controls enforced outside the model: tool and object authorization, parameter schemas, outbound access, sandboxing, output validation and approval bound to the specific action.

4. Measure legitimate task completion, prohibited actions and disclosure separately. Repeat stochastic cases and record model, parameters, budget and dataset version. An agent that fails every task has not demonstrated useful protection.

5. Check loops, delegation, costs, cancellation and retries. Review secondary agents and composed tools; a limit on the first agent cannot protect a tool that bypasses it.

6. Use the [targeted verification cases](../agent-boundaries.md) when this surface is present. Select cases for the actual architecture and record the observed limits.

## Required evidence

Provide sanitized tool-call traces, preconditions, observed outcomes and benign test cases. Keep product evaluation results separate from published benchmark scores.

## Tools and limits

PyRIT, garak and AgentDojo provide test frameworks to adapt. Hosted models incur costs and transfer data; use synthetic fixtures and an authorized provider.

## References

- [OWASP GenAI LLM Top 10](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/): 2026, August 2026.
- [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/): 2026.
- [AgentDojo paper](https://arxiv.org/abs/2406.13352): 2024; check revisions.
- [Indirect Prompt Injections: Are Firewalls All You Need, or Stronger Benchmarks?](https://arxiv.org/abs/2510.05244): 2025; evaluation metric critique.
- [Microsoft PyRIT](https://github.com/microsoft/PyRIT): External tool reference.
- [NVIDIA garak](https://github.com/NVIDIA/garak): External tool reference.

For recent requirements or vulnerabilities, use the [research method](../../../cyber-audit/references/research-policy.md).

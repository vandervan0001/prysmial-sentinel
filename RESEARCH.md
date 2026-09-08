# Research baseline: 8 September 2026

The library contains original procedures, selected third-party documentation and normalized MITRE data. The upstream repository review checked owner, HEAD commit, activity date, archived status and declared licence. It did not audit their code.

## Standards and current references

- ASVS 5.0.0 provides versioned application security requirements. OWASP lists it as stable. Use a requirement identifier only after checking its wording in the source. [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).
- NIST SP 800-63-4, finalized in July 2025, and RFC 9700, published in January 2025, inform the identity, federation and OAuth methods. Apply them according to the service and required assurance level. [NIST](https://csrc.nist.gov/pubs/sp/800/63/4/final), [IETF](https://www.rfc-editor.org/rfc/rfc9700.html).
- OWASP published the GenAI LLM Top 10 2026 in August 2026. The AI methods also examine agent permissions, MCP trust boundaries, tools, memory and controls enforced outside the model. [OWASP GenAI](https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/).
- FIPS 203 is the reference for ML-KEM preparation. The cryptography method checks the primitive, library, protocol and tested integration separately. [NIST](https://csrc.nist.gov/pubs/fips/203/final).

Pages under `latest` can change. The Solidity page reviewed here showed a development version, so the method requires documentation matching the target compiler. The final review updated SLSA references to approved version 1.2 and its source and build tracks. [SLSA 1.2](https://slsa.dev/spec/v1.2/).

## Research and agent evaluation

[AgentDojo](https://arxiv.org/abs/2406.13352) and [Agent Security Bench](https://arxiv.org/abs/2410.02644) provide test scenarios and evaluation approaches. The AI methods assess legitimate task completion and unwanted effects separately, using tool traces and synthetic data.

[Indirect Prompt Injections: Are Firewalls All You Need, or Stronger Benchmarks?](https://arxiv.org/abs/2510.05244) examines benchmark and metric limitations. The AI method requires benign test cases, observable outcomes and a coverage assessment before drawing a conclusion about protection.

[AgentSecBench](https://arxiv.org/abs/2605.26269) and [Runtime Skill Audit](https://arxiv.org/abs/2606.11671) are 2026 research references for authority boundaries, confidentiality and skill effects. Their results have not been reproduced here. Published scores are not performance claims for this library.

## Upstream selection

The [repository registry](skills/cyber-audit/references/repositories.json) records 27 repositories and their commits. Their roles are:

- MITRE: an offline Enterprise, ICS and Mobile index. CAPEC remains a separate external reference.
- Trail of Bits: eight selected documentation sets, with resources and licence retained.
- OWASP and Semgrep collections: AppSec references. The six executable rules bundled here are local and tested.
- ProjectDiscovery, PayloadsAllTheThings and HackTricks: references for choosing test hypotheses and procedures within scope.
- OTRF, Sigma, Atomic, Elastic, Splunk and Velociraptor: hunting, detection, validation and investigation references.
- ITI, ICS indexes, Wireshark, OPC Foundation and vendor portals: industrial review references.

The registry uses the official `splunk/security_content` repository in place of the proposed `rkondracki/security-content` fork. Licences vary across collections. Content without a reviewed licence and adaptation remains linked, without bulk copying or execution. [Splunk repository](https://github.com/splunk/security_content), [Semgrep rule terms](https://github.com/semgrep/semgrep-rules).

## What was verified

All 50 initial links were accessible during the HTTP check. That records availability at the time of the check; scientific quality requires reading the relevant source. Library tests cover method selection, data formats, control records, local queries and bundled rules. No live service pentest or physical controller test was performed.

## Final review

The [literature review](LITERATURE_REVIEW.md) records the material inspected and its effect on the methods. The registry now includes 59 references. All 59 were accessible across the final 57-source check and two-source supplement.

Added references cover SSDF, HTTP/1.1, SSRF, ML-DSA, SLH-DSA, Sigma, ACS and the OWASP GenAI crosswalk. SSDF 1.2 remains marked as a draft. The new guides use these sources for bounded test designs; research scores and framework mappings are not imported as claims about Sentinel.

Original analysis also identified defects in the importer and report pipeline. The [synthetic example](examples/review-lab-report.md) demonstrates authorization and state failures through real local calls. Its observed results are separate from the cited research experiments.

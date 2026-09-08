# Telemetry and detection test design

Use this procedure before concluding that a hunt found nothing or a rule provides coverage. Start with one known event in the selected population and time range.

| Stage | Positive control | Failure case to distinguish |
|---|---|---|
| Generation | Expected behavior produces the source event | Wrong audit configuration or behavior never executed |
| Collection | Event reaches the collector with its identity | Host absent, sampling, dropped event or retention gap |
| Parsing | Required fields survive normalization | Missing field, null, wrong type, renamed field or truncated content |
| Query | Known event matches in the deployed engine | Conversion error, empty data model, wrong index or time basis |
| Correlation | Ordered events match within the chosen window | Late arrival, clock skew, duplicate or out-of-order delivery |
| Alert | A result creates the expected alert | Deduplication, suppression, disabled rule or muted route |
| Delivery | Authorized test recipient receives the alert | Notification transport failed after alert creation |

For Sigma conversion, record rule revision, processing pipeline, backend and schema. For an ECS/CIM mapping, compare the source and normalized event values. Test missing fields and case semantics in the actual query language; do not infer them from the source YAML. [Sigma specification](https://sigmahq.io/sigma-specification/).

Keep benign events that resemble the suspicious behavior. Report hits and total relevant events separately; a false-positive percentage without a population is uninterpretable. Distinguish rules tested with stored events from detections verified in the running pipeline.

For a negative hunt, list reachable hosts/accounts, time boundaries, ingestion delay and the fields that could reveal the behavior. Preserve alternative explanations. An ATT&CK mapping identifies the behavior of interest but does not establish detection efficacy. [MITRE ATT&CK](https://attack.mitre.org/).

Send collector defects and query defects to their respective owners with the same minimal event. A saved event cannot demonstrate live collection or delivery. Reuse the [purple-team procedure](../../cyber-purple-team/references/domain.md) when those stages need authorized execution.

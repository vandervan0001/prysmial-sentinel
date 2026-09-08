# Detection rules and SIEM integration

Detection covers rules, telemetry requirements, backend conversion and tests. Hunting investigates hypotheses. Purple team verifies the full path to alert delivery in a controlled environment.

## Sigma and telemetry

Start with the behavior and log source. Define product, service, category, fields, identity and correlation window. Pin the Sigma rule and conversion pipeline versions. A Sysmon `Image` field does not automatically map to an equivalent ECS or CIM field.

Review SigmaHQ rules and metadata before reuse. Retain identifier, version, status, known false positives and file licence. Test positive and benign events before activation. Preserve experimental or overly broad rule status in the report.

## Elastic and Splunk

For Elastic, check ECS, Fleet/Agent integration, index or data stream, query language, interval, lookback, timestamps, exceptions and deduplication. Test import and execution in a laboratory space. The `elastic/detection-rules` repository has its own tooling and licence terms; do not assume Apache or MIT.

For Splunk, use the official `splunk/security_content` repository. Check sourcetypes, CIM, data models, acceleration, macros and mappings. An empty `tstats` search can result from an unpopulated model. Find a known event in the raw index and then in the model. An Analytic Story provides context; it does not establish that the associated detections are active.

## YARA and artifacts

Define the file family, classification objective and YARA/YARA-X version. Choose discriminating strings, anchors and size bounds. A generic marker from a legitimate tool is insufficient to classify malware. Compile the rule, measure cost, test an authorized malicious corpus and a benign corpus, and retain false-positive results.

Yara-Rules and ANY.RUN provide references. Public rules do not imply a common licence across a collection. Do not submit client files to public analysis services by default.

Sources and commits are in the [shared registry](../../cyber-audit/references/repositories.json). Report each rule with its engine, telemetry, fixtures and the alert delivery result actually tested.

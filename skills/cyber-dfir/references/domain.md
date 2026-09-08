# Endpoint evidence and suspicious artifacts

DFIR covers preservation, targeted collection, analysis and timelines. Start from hunting or detection signals and establish the facts needed for containment.

## Collection

Define the question before selecting an artifact: connection, process, persistence, file, browser, memory or configuration history. Record platform, location, volatility, required permissions and limits. Avoid full collection when a specific artifact answers the question.

For [Velociraptor](https://github.com/Velocidex/velociraptor), select the artifact definition and version, parameters, VQL sources, permissions and preconditions. Read the called functions; some artifacts execute commands or transfer files. A `Windows` or `Linux` prefix does not guarantee read-only behavior. Estimate expected output and volume before endpoint deployment.

Preserve hash, source, collection identifier, time and timezone. Keep the original separate from transformed copies. Check whether system, event and ingestion timestamps describe the same occurrence.

## Suspicious files

Start with hash, actual type, structure, signature, imports and metadata. Extract in an isolated environment with resource limits. For documents, inspect links, macros and embedded content without opening the application that could execute them.

YARA and antivirus results need context. Distinguish family identification, similarity, capability and observed behavior. If dynamic analysis is necessary and authorized, use a disposable laboratory without credentials or client network access, with monitoring and controlled outbound access.

Public sandbox submission requires permission to share the artifact. Report facts, indicators, confidence and proposed actions. Static analysis does not establish every runtime behavior.

The [incident response method](modules/incident.md) covers timelines, containment and recovery. Send rule corrections to `cyber-detection` with the corpus and control cases.

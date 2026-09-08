# Detection chain validation

Validate a selected scenario in an authorized laboratory. A request to review detections does not by itself authorize Atomic Red Team execution.

1. Choose a specific behavior, technique and detection objective. Define the expected event, required fields, rule, acceptable delay and alert recipient.
2. Select an [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) test by GUID and commit. Read commands, dependencies, permissions, platforms, downloads, arguments, artifacts and cleanup. Tests for the same technique can have very different effects.
3. Prepare a minimal laboratory variant with synthetic files and identities. Use harmless telemetry generation when it meets the objective. Do not install or invoke every atomic test automatically.
4. Execute the explicitly covered scenario with limits and a stop condition. Verify behavior, event ingestion, rule matching and delivery to the authorized recipient separately.
5. Run a benign control to assess noise. Verify cleanup and final state, including dependencies and files created by the test.
6. If no alert arrives, locate the failed stage: generation, collection, normalization, query, window, suppression or delivery.

Deliver a test GUID/version → behavior → event → rule → alert matrix, with a timestamp and result at each stage. An Atomic test exiting with code 0 does not establish the intended effect. A saved positive event supports rule unit tests, but does not replace validation of the running detection chain.

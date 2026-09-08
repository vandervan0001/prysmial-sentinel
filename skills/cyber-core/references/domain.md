# References and evidence assessment

Core defines vocabulary, evidence requirements, research methods and priorities. Technical verification belongs to the relevant domain. An ATT&CK mapping describes behavior; it does not establish a vulnerability, group attribution or compromise.

## Local ATT&CK index

`attack/index.json` contains selected techniques, mitigations, tactics, detection objects and relationships from Enterprise, ICS and Mobile. Revoked and deprecated objects are excluded. [provenance.json](attack/provenance.json) records the repository, commit and transformations. The [MITRE licence](attack/LICENSE.txt) is included. This is a normalized index, not a complete STIX bundle.

From the library directory:

```bash
python3 skills/cyber-core/scripts/knowledge.py attack T1059 --domain enterprise-attack
python3 skills/cyber-core/scripts/knowledge.py attack "Modify Controller Tasking" --domain ics-attack
python3 skills/cyber-core/scripts/knowledge.py controls --domain cyber-ot --protocol modbus
```

For each mapping, retain the domain, technique identifier and URL, observed behavior and confidence. Do not conflate equal identifiers across domains. Relationships can reference objects absent from this selected index; query results identify unresolved endpoints.

ATT&CK describes adversary behavior, CWE weakness classes, CAPEC attack patterns and ASVS verification requirements. A shared word does not establish an official mapping. CAPEC is an external reference to check when needed and is not included in the ATT&CK snapshot. Verify the dataset before presenting `mitre/cti` as a CAPEC source.

## Structured controls

The [compiled catalogue](controls.json) records applicability, procedure, evidence, references and execution conditions. The [schema](control.schema.json) defines its fields. Records support method selection and audit planning; they neither run tools nor grant permissions.

Select a control for the asset and property under review, record context and pass the question to the responsible domain. Return evidence and status under the shared contract. Calculate coverage against selected controls, not the full catalogue size.

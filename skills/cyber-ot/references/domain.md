# Industrial review by process and system boundary

OT covers the physical process, operating constraints, segmentation and equipment behavior. Select methods from the observed process, exports and network. A reachable controller still requires a test approach matched to its physical effects.

| Available input | Method |
|---|---|
| Architecture and maintenance access | [OT architecture](modules/ot.md) |
| Software image and update chain | [Firmware](modules/firmware.md) |
| Network capture or flow list | [Protocols and network analysis](protocols.md) |
| Model, part number, firmware and engineering tools | [Vendor checks](vendors.md) |
| Zone, supplier or integrator requirements | [IEC 62443 applicability](iec62443.md) |

Start with the consequences of an incorrect command, loss of supervision or interruption. Map owners, zones, flows, remote access, engineering workstations, backups and safety functions. An incomplete controller export cannot establish the process limits.

Query ICS techniques in the [local reference](../../cyber-core/references/domain.md), then select relevant [structured controls](../../cyber-core/references/controls.json). An ICS technique describes possible behavior; feasibility still depends on the equipment model.

ITI/ICS-Security-Tools and the registered ICS lists provide leads. Check older utilities, captures and scripts for date, protocol, version, licence and behavior before reuse. Third-party PCAPs may contain real data; use authorized excerpts or synthetic captures. The library does not replay these captures or run their executables.

Report gaps by zone and equipment, with potential effect, offline evidence, compensating control and next measurement. Physical tests require a specific mandate, operating window, restorable backup and suitable stop procedure.

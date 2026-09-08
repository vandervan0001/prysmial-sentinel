# Protocols and offline network analysis

Review existing captures with their time, capture point, direction, loss and duration. A known port suggests a protocol; confirm it through decoding, peer roles and consistent exchanges. A capture from the wrong SPAN cannot establish that a flow was absent.

Hash the capture and work on a copy. Use `-n` to avoid name resolution during Wireshark/tshark analysis. Available fields depend on version; check the installed engine's help and protocol list.

```bash
tshark -n -r /path/capture.pcapng -q -z io,phs
tshark -n -r /path/capture.pcapng -Y modbus -T fields -e frame.number -e frame.time_epoch -e ip.src -e ip.dst
```

These examples read a file and use display filters, not BPF capture filters. Verify compatibility with the actual capture and tshark version before relying on the result.

| Protocol | Decoder to verify | Review questions |
|---|---|---|
| Modbus/TCP | `modbus`, `mbtcp` | Client/server roles, observed functions, reads/writes, ranges, exceptions and segmentation |
| S7 | `s7comm`, variant by generation | Engineering workstations, programming, reads/writes, CPU protection and access trust |
| PROFINET | `pn_io`, `pn_dcp` as applicable | Controller/device relationships, discovery/configuration, name/IP changes and local layer-2 access |
| EtherNet/IP and CIP | `enip`, `cip` | Explicit/implicit connections, roles, administrative operations and actual CIP Security support |
| OPC UA | `opcua` by transport | Endpoints, policies, mode, certificates, user identity, roles, trust list and revocation |
| DNP3 or IEC 60870-5-104 | Check installed dissector and fields | Control roles, commands, timestamps, identity validation and segmentation |

## Modbus and S7

Build a source → destination → function → volume → period matrix. Distinguish expected process traffic from maintenance. For an observed write, map the register or object to the supplied project and naming scheme. Without that source, a register number does not identify its physical function.

Avoid blanket encryption claims about Modbus or S7 generations. Establish protocol, mode, protections, version and any gateway. Include network boundaries, roles and engineering workstations in the analysis. Test writes require a laboratory bench or an explicitly prepared physical intervention.

## OPC UA

Compare advertised and used endpoints, SecurityPolicy, MessageSecurityMode, application trust, user identity and node authorization. A SignAndEncrypt channel does not establish least privilege for the user. Review automatic certificate acceptance, expiry, rejection and renewal from configuration or a laboratory server.

## Captures and detection

For each anomaly, retain frame numbers, filter, endpoints and an alternative explanation. Read captures in an offline analyzer or rule test without reinjecting traffic into the industrial network. For Zeek/Suricata, identify parser, version, fields and required positive/negative events before proposing a detection.

Primary sources: [Wireshark Modbus reference](https://www.wireshark.org/docs/dfref/m/modbus.html), [S7comm reference](https://www.wireshark.org/docs/dfref/s/s7comm.html), [EtherNet/IP reference](https://www.wireshark.org/docs/dfref/e/enip.html), [OPC UA security model](https://reference.opcfoundation.org/Core/Part2/v105/docs/).

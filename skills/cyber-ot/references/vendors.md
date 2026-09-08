# Vendor-specific checks

Identify the part number, firmware, options and engineering tool version before recommending changes. Retain advisory date, affected versions, preconditions and vendor fix. A product family named in an advisory does not establish that every installed device is affected.

| Vendor | Primary source | Project evidence and checks to adapt |
|---|---|---|
| Siemens | [ProductCERT](https://cert-portal.siemens.com/) | CPU/HMI reference, firmware, TIA/STEP 7/WinCC version, protection levels, enabled services, program transfers, certificates and backups |
| Rockwell Automation | [Trust Center](https://www.rockwellautomation.com/en-us/trust-center.html) | Controller family, firmware, Studio 5000/FactoryTalk, roles, operating modes, maintenance access, CIP services and documented security capabilities |
| Schneider Electric | [Cybersecurity portal](https://www.se.com/ww/en/work/support/cybersecurity/overview.jsp) | Controller/HMI range, firmware, Control Expert/Machine Expert as applicable, services, engineering access, certificate management and fixes |
| Omron | [Product Security](https://www.fa.omron.co.jp/product/security/en/) | Family, firmware, Sysmac/CX as applicable, Ethernet services, programming permissions, remote maintenance and backup strategy |

Complete a device record with verified identity, files reviewed, current access, applicable or unresolved advisories, compensating controls and required tests. Do not assume an older controller supports a feature from a newer range.

Where an update cannot fit the available window, assess exposure, permitted access, segmentation, monitoring and restoration as compensating measures. Claim that a measure addresses a CVE only when its effect on that vulnerability's mechanism has been demonstrated.

Program and parameter changes remain offline proposals until loading is authorized. Final verification requires an identified backup, rollback procedure, process validation and checks against the version actually loaded.

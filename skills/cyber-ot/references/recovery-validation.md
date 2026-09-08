# OT recovery and change verification

Use this procedure when reviewing backups, updates, remote maintenance or incident recovery. Start with process constraints and the equipment version. NIST SP 800-82 rev. 3 treats OT safety, reliability and availability as operating constraints; an IT recovery sequence cannot be assumed suitable for a controller. [NIST OT guidance](https://csrc.nist.gov/pubs/sp/800/82/r3/final).

## Evidence by layer

| Layer | Evidence | Remaining limit |
|---|---|---|
| Backup exists | Identified program, parameters, firmware, licences and hashes | Existence does not establish restorability |
| Offline restore | Vendor tool opens the backup with dependencies resolved | Does not establish behavior on the installed controller |
| Laboratory restore | Identified bench restores configuration and test behavior | Simulator and hardware may differ from the process |
| Physical validation | Authorized test against the loaded version and observed process state | Applies to that operating window and tested conditions |

Record which state is persistent, volatile, recipe-controlled or owned by another device. Include certificates, trusted peers, engineering access and historian/supervision dependencies. Restore tests use a prepared bench; do not overwrite production to assess a backup.

For a proposed change, compare intended values, encoded representation, transferred artifact and readback. Check units, signedness, byte/word order, scaling, bounds and invalid values where relevant to the protocol. A successful transfer only proves that the transfer completed. Define the process observation that establishes correct behavior.

Review remote maintenance through its whole lifecycle: approval, named identity, path opened, recorded access, expiry and removal. Test expiration on a laboratory path while preserving the operational fallback procedure. An account disabled in one directory may leave another credential or session active.

For incident recovery, separate preserved evidence, containment, restoration and confirmation that the original cause has been removed. Record the operator responsible for process acceptance and the criteria for stopping. [NIST incident response](https://csrc.nist.gov/pubs/sp/800/61/r3/final).

This is a Sentinel verification procedure. It neither supplies IEC 62443 requirement numbers nor replaces vendor instructions, safety engineering or process acceptance.

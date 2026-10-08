# Kavitha Sekar — transferable-skills mapping

## Positioning statement

The purpose of this project is not to claim previous avionics test experience.
It demonstrates how existing electronics/instrumentation and network-security experience
transfers into systems integration, verification and datalink test engineering.

| Existing evidence | Transfer to avionics test | OpenDLab evidence to create |
|---|---|---|
| Electronics & Instrumentation degree | measurement chains, interfaces, sensors, test mindset | ARINC429 HIL loopback + signal/timing measurements |
| IP port approvals | interface control and authorized communication paths | default-deny datalink policy + interface matrix |
| Least privilege / whitelisting | secure communications architecture | source/destination/service allowlists |
| Temporary permission management | controlled configuration / expiry discipline | time-bounded test configuration and rollback procedure |
| Nmap service discovery | interface verification and unintended-service detection | scan only isolated lab nodes before/after config changes |
| Nessus vulnerability assessment | structured negative/security testing | lab vulnerability test plan; no scanning real aircraft systems |
| CVE/CVSS reporting | anomaly severity and engineering decision support | severity matrix for test anomalies and go/no-go review |
| ISO 27001 documentation | traceability, evidence retention, auditability | configuration baseline, hashes, test evidence manifest |
| Wireshark | protocol-level troubleshooting | PCAP correlation with application and router logs |
| SIEM/Sentinel | event correlation | event timeline / anomaly dashboard |
| ServiceNow | defect/change workflow | GitHub Issues with severity, owner, disposition and evidence |
| Cross-functional remediation | collaboration with design stakeholders | defect report written as input to a Design Office |
| CCNA learning | IP routing / network fundamentals | IPv6, network namespaces, FRRouting and failover tests |

## Application narrative

A credible interview narrative is:

1. My original professional domain was network security and controlled change.
2. That work taught me to verify interfaces before approval, identify unexpected exposure,
   evaluate risk, document decisions and maintain an audit trail.
3. I built OpenDLab to deliberately transfer those disciplines into an avionics context.
4. I added aircraft-style communication flows, ARINC429 learning, bearer failover, test
   procedures, instrumentation, PCAP analysis, configuration control and negative testing.
5. I can therefore show practical evidence of how I learn an unfamiliar technical system
   and convert requirements into repeatable verification activities.

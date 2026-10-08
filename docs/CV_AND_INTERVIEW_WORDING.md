# CV and interview wording

Use these only after the stated work has actually been completed.

## CV project entry

### OpenDLab-Secure — Avionics Datalink Integration & Cyber Test Bench
Independent open-source upskilling project

- Designed a requirements-driven home avionics test bench simulating aircraft applications,
  a datalink router, multiple communication bearers and a ground endpoint.
- Reused network-security experience to implement least-privilege source/destination/service
  policies, configuration-baseline checks, negative tests and traceable anomaly reporting.
- Developed automated Python/pytest verification for functional routing, bearer failover,
  malformed/unauthorized traffic and ARINC429 word/parity handling.
- Used Wireshark/tcpdump and structured event logs to correlate protocol traffic with system
  behaviour and produce repeatable test evidence.
- Built requirements-to-test traceability and engineering test reports covering nominal,
  degraded and fault-injection scenarios.
- Extended networking knowledge toward IPv6/ATN-IPS-inspired routing and communication
  continuity testing in an isolated Linux lab.

## 60-second interview answer

“My previous professional experience is in network security rather than aircraft testing.
The transferable part is the verification discipline: before approving connectivity I had
to understand the requested interface, identify services and exposure, evaluate technical
risk, document the decision and maintain an auditable record. I built OpenDLab to apply that
same discipline to an avionics-style environment. I created aircraft and ground simulators,
a datalink router, multiple degraded communication paths, security-negative tests, packet
instrumentation and configuration control. I then added ARINC429 learning and formal
requirements-to-test traceability. The project lets me demonstrate both what I already bring
and how I am closing the avionics-specific gap.”

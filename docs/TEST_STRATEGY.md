# OpenDLab Test Strategy

## 1. Purpose
Demonstrate a repeatable integration-test approach for an airborne datalink router and
multiple simulated air/ground communication means.

## 2. System under test
The SUT is the educational OpenDLab datalink router and its interfaces:
- aircraft application messages
- ARINC429-like input adapter
- multiple IP communication bearers
- ground gateway

## 3. Test levels
1. Unit test
2. Software integration test
3. Network/bearer integration test
4. Hardware-in-the-loop ARINC429 loopback
5. Mission-profile test
6. Regression campaign

## 4. Key quality attributes
- functional correctness
- message integrity
- end-to-end latency
- continuity during bearer failure
- deterministic handling of malformed input
- observability
- repeatability
- requirements traceability

## 5. Entry criteria
- code builds
- unit tests pass
- configuration frozen and tagged
- time synchronization checked
- capture/log directory cleared
- test environment documented

## 6. Exit criteria
- planned cases executed
- no open severity-1 defects
- KPI thresholds assessed
- anomalies dispositioned
- report generated
- configuration and evidence archived

## 7. Fault injection
Use Linux netem or isolated namespace/container interfaces to inject:
- delay and jitter
- packet loss
- duplication
- corruption
- reordering
- bandwidth constraint

## 8. Evidence
For each campaign archive:
- Git commit SHA
- configuration files
- test results
- JSONL event logs
- PCAP
- defect notes
- KPI summary
- final engineering conclusion

## 9. Limitations
This project is a learning bench and is not a certification environment.
Values chosen for simulated bearers are illustrative and must not be represented as
certified or operational Airbus performance data.

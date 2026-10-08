# Requirements-to-Test Traceability

| Requirement | Verification method | Test |
|---|---|---|
| R-DL-001 Router shall forward a valid operational message | Integration test | DL-NOM-001 |
| R-DL-002 Router shall select a healthy bearer | Automated test | DL-FAIL-002 |
| R-DL-003 Router shall expose forwarding events | Inspection + test | DL-NOM-001 |
| R-A429-001 Decoder shall verify odd parity | Unit test | A429-PAR-006 |
| R-A429-002 Decoder shall expose label/data/SSM/SDI | Unit test | A429-LBL-007 |
| R-NET-001 Test bench shall support link delay/loss injection | Demonstration | DL-LAT-003 |
| R-IPS-001 Lab shall support IPv6 routing experiment | Demonstration | IPS-BGP-008 |
| R-QOS-001 High-priority service shall receive preferred treatment | Performance test | QOS-009 |
| R-SEC-001 Invalid source/input shall be rejected and logged | Negative test | SEC-010 |

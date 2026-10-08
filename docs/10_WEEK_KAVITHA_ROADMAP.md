# Kavitha-focused 10-week roadmap

The ordering is chosen to reuse existing strengths first, then progressively add avionics-specific
knowledge. This creates demonstrable progress early.

## Week 1 — network test bench from familiar skills
- Run aircraft/router/ground software.
- Capture traffic in Wireshark.
- Produce an interface control table: source, destination, protocol, port, purpose.
- Demonstrate default-deny policy.

**Portfolio proof:** PCAP + interface matrix + 5 automated tests.

## Week 2 — configuration control and audit trail
- Create campaign configuration manifest and SHA-256 baseline.
- Add Git tags and a test-run evidence folder.
- Use GitHub Issues as the defect/change log.

**Transfer:** ISO 27001 / exception logging -> controlled test configuration.

## Week 3 — security-negative testing
- Test unauthorized source, unauthorized service, malformed payload and unexpected open service.
- Run Nmap only against the isolated lab.
- Write one risk report using severity, impact and go/no-go reasoning.

**Transfer:** Nmap/Nessus/CVSS/reporting -> verification/anomaly disposition.

## Week 4 — formal V&V discipline
- Create 20 requirements.
- Build requirements-to-test traceability.
- Add preconditions, steps, expected result, actual result and verdict.
- Create a test readiness checklist.

**New skill:** formal systems test preparation.

## Week 5 — bearer failure and network impairment
- Add Linux namespaces and netem.
- Model VDL2-like and SATCOM-like paths.
- Measure latency, jitter, loss and failover.
- Use Wireshark to explain one failed test.

**Transfer:** packet/network troubleshooting -> datalink integration test.

## Week 6 — ARINC429 fundamentals
- Learn word format, labels, SDI, SSM and parity.
- Extend automated tests.
- If possible, start Pico/RP2xxx isolated TX/RX loopback.

**Transfer:** Electronics & Instrumentation -> avionics interface testing.

## Week 7 — physical HIL
- Complete ARINC429 isolated loopback.
- Measure expected/received word counts and timing.
- Inject bad parity and unexpected labels.
- Document wiring and bench limitations.

**Portfolio proof:** bench photo + procedure + raw evidence.

## Week 8 — IPv6 / ATN-IPS-inspired networking
- Create IPv6 aircraft/provider/ground domains.
- Introduce FRRouting.
- Withdraw a route and measure reconvergence.
- Relate the exercise to communication continuity, not to certified ATN implementation.

**Transfer:** CCNA/networking -> next-generation avionics connectivity.

## Week 9 — integrated mission campaign
- Drive a flight profile manually or through FlightGear.
- Execute 25–30 test cases.
- Freeze configuration.
- Collect PCAP, JSONL, plots and defect records.

## Week 10 — Airbus application package
- Produce a 6–10 page test report.
- Record a 4-minute demo.
- Publish a sanitized GitHub release.
- Add the project to CV and LinkedIn.
- Practice 10 interview questions focused on test reasoning and transferable skills.

## Parallel activity — French

The target vacancy asks for advanced/fluent French. Treat French improvement as a separate
critical workstream; the technical project does not compensate for the language requirement.

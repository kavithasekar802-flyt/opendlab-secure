# How to substantiate OpenDLab in an application

Do not describe this as an Airbus-equivalent bench. Describe it as an independent,
open-source learning/test platform.

## CV project title
**OpenDLab — Home Avionics Datalink & Communication Integration Test Bench**

## Suggested CV bullets
- Designed and implemented an open-source avionics integration test bench simulating an
  airborne datalink router, aircraft applications, multiple air/ground communication
  bearers and a ground endpoint.
- Authored requirements, test strategy and automated regression procedures covering
  nominal operation, bearer failover, latency/loss/corruption, message integrity and
  post-test analysis.
- Implemented ARINC 429 educational word packing/decoding with label, SDI, SSM and odd
  parity validation and prepared a hardware-in-the-loop expansion using an RP2xxx
  transceiver prototype.
- Built IPv6/ATN-IPS-inspired routing experiments and measured failover/reconvergence
  using packet capture and structured instrumentation.
- Used Python, pytest, Linux networking, Wireshark/tcpdump and open-source aviation
  tooling to generate traceable engineering evidence and maturity-style test reports.

## Interview demo sequence
1. Show architecture and traceability matrix.
2. Run normal message flow.
3. Disable VDL2_SIM and demonstrate automatic fallback.
4. Apply netem impairment and compare latency KPIs.
5. Inject ARINC parity fault and show rejection.
6. Open PCAP in Wireshark and correlate with JSONL timestamps.
7. Show one defect/root-cause report.
8. Explain limits of the bench and what would change for a certified industrial setup.

## Evidence that matters more than code volume
- a coherent test strategy
- reproducible campaign
- disciplined test configuration
- raw evidence
- anomaly/root-cause reasoning
- engineering report
- limitations stated clearly

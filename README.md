# OpenDLab — Open Datalink & Communication Systems Integration Test Bench

**OpenDLab** is a home-lab, open-source avionics upskilling project designed to demonstrate
skills relevant to aircraft datalink and communication systems integration/test engineering.

It is deliberately a **lab/simulation project**. It is **not airworthy equipment** and must
not be connected to, installed in, or used to control a real aircraft.

## What this project demonstrates

- Test strategy definition and traceability
- Lab test means architecture
- Avionics datalink routing concepts
- ARINC 429 word generation/decoding fundamentals
- IPv6 / ATN-IPS-inspired networking
- Multiple simulated air/ground communication bearers
- Automated test procedures
- Fault injection: latency, loss, corruption, duplication, reordering
- Instrumentation: packet capture, structured event logs and KPIs
- Post-test analysis and maturity reporting
- Optional passive ACARS/VDL2 observation with SDR
- Optional FlightGear integration
- Optional anomaly detection / AI-assisted test analysis

## Safety / legal boundary

1. **Do not transmit on aviation VHF/HF/SATCOM frequencies.**
2. The SDR extension in this project is receive-only.
3. ARINC 429 hardware is for isolated bench loopback only.
4. This project does not implement a certified Airbus system or proprietary Airbus design.
5. Public descriptions of ARINC/ICAO concepts are used only for learning. Obtain the official
   standards where required; do not treat this repository as a substitute for them.

---


## Candidate positioning — Kavitha Sekar

This fork is deliberately tailored to demonstrate a credible transition from **network/security
operations into avionics integration testing**.

Existing transferable evidence:
- B.E. Electronics & Instrumentation Engineering
- network access / port-change assessment and approval
- Nmap service discovery and Nessus vulnerability assessment
- CVE/CVSS-based technical risk reporting
- ISO 27001 control discipline and audit trails
- source/destination whitelisting and least-privilege thinking
- Wireshark, SIEM and ServiceNow exposure

Therefore the portfolio emphasis is:

**secure communications integration + disciplined verification + instrumentation + anomaly
analysis + configuration control**, rather than claiming prior aircraft test experience.

The project must remain clear about the gap: avionics protocols, formal V&V, physical ARINC
interfaces and aviation test practice are newly acquired skills demonstrated through this lab.

---

# 1. Architecture

```text
+----------------------- AIRCRAFT LAB -----------------------+
|                                                            |
|  Flight profile /      A/C App Simulator                   |
|  FlightGear ----------> FMS/AOC/ACMS-like messages        |
|                              |                             |
|                     +--------v---------+                   |
|  ARINC429 emulator ->| Datalink Router |<-- health/QoS    |
|  or Pico loopback     +--+----------+--+                   |
|                         |          |                       |
+-------------------------|----------|-----------------------+
                          |          |
                 "VDL2-like"      "SATCOM-like"
                  low latency      high latency
                  constrained      resilient
                          |          |
                    Linux netem / namespaces
                          |          |
+-------------------------|----------|-----------------------+
|                     +---v----------v---+                   |
|                     | Ground Gateway   |                   |
|                     +--------+---------+                   |
|                              |                             |
|                       ATC/AOC Simulator                    |
|                                                            |
+----------------------- GROUND LAB -------------------------+

Instrumentation:
tcpdump/Wireshark + JSONL event logs + test-run artifacts + KPI report
```

## Recommended progression

### Level 1 — Software-only bench
Run the complete simulated aircraft → router → ground chain on one Linux host.

### Level 2 — Network impairment bench
Create Linux network namespaces and use `tc netem` to model multiple bearers.

### Level 3 — Physical ARINC 429 loopback
Add an RP2040/RP2350-based low-cost ARINC-429 proof-of-concept interface or a commercial
USB/Ethernet ARINC adapter. Keep the circuit isolated from real aircraft equipment.

### Level 4 — Passive datalink observation
Use a receive-only SDR with `dumpvdl2` / `libacars` to compare real-world message/protocol
structures with your simulated test data. Never transmit.

### Level 5 — Flight profile integration
Use FlightGear to drive phase-of-flight changes, position, altitude and bearer policies.

### Level 6 — ATN/IPS-inspired lab
Create IPv6 routing domains with FRRouting and test routing convergence, QoS and multilink failover.

---

# 2. Quick start

Designed for Ubuntu 24.04 or WSL2 Ubuntu.

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip iproute2 tcpdump wireshark
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

Open three terminals:

```bash
source .venv/bin/activate
python -m src.ground_station
```

```bash
source .venv/bin/activate
python -m src.datalink_router
```

```bash
source .venv/bin/activate
python -m src.aircraft_app
```

The aircraft application emits operational-style datalink messages. The router selects a bearer,
forwards them to the ground station, and records structured events in `artifacts/`.

---

# 3. Suggested portfolio test campaign

| ID | Objective | Stimulus | Expected result | Evidence |
|---|---|---|---|---|
| DL-NOM-001 | Nominal uplink/downlink | 100 normal messages | 100% delivery | JSONL + pcap |
| DL-FAIL-002 | Bearer loss | Disable preferred bearer | Automatic fallback | routing event |
| DL-LAT-003 | SATCOM-like delay | +600 ms delay | delivery within threshold | latency histogram |
| DL-LOSS-004 | Loss resilience | 2% random loss | retries / loss detected | KPI report |
| DL-CORR-005 | Corruption handling | packet corruption | malformed message rejected | negative test log |
| A429-PAR-006 | ARINC parity | inject wrong parity | invalid word detected | unit test |
| A429-LBL-007 | Label filtering | unexpected label | rejected / quarantined | trace log |
| IPS-BGP-008 | IPv6 route loss | withdraw route | reconvergence measured | pcap + BGP log |
| QOS-009 | Priority handling | ATS vs maintenance | ATS prioritized | queue latency |
| SEC-010 | Unauthorized sender | invalid endpoint/token | message rejected | security log |
| FLT-011 | Mission profile | climb/cruise/approach | policy changes correct | timeline |
| AI-012 | Anomaly assistance | mixed failures | anomaly model flags outliers | notebook/report |

---

# 4. Definition of done

A portfolio release should contain:

- `TEST_STRATEGY.md`
- requirements-to-test traceability matrix
- architecture diagram
- automated regression suite
- at least 25 test cases
- at least 5 negative/fault-injection tests
- Wireshark/tcpdump captures
- latency/loss/failover KPIs
- one failed test with root-cause analysis
- one test-means limitation / uncertainty analysis
- one 5–10 page engineering test report
- a 3–5 minute bench demonstration video
- tagged GitHub release, e.g. `v1.0-test-campaign`

The objective is not to claim certification. The objective is to demonstrate disciplined
systems-integration and test-engineering thinking.

---

# 5. Repository layout

```text
src/                    runnable Python bench
tests/                  automated unit/integration tests
configs/                bearer and flight-profile configuration
scripts/                network impairment helpers
docs/                   strategy, test plan and portfolio documentation
artifacts/               generated run logs (gitignored except README)
hardware/                ARINC429 bench notes
```

## License

MIT for original code in this repository. Third-party tools retain their own licenses.

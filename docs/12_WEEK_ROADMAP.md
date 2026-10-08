# 12-week upskilling roadmap

## Weeks 1–2 — foundations
- Read public material on ACARS, VDL2, ATN/OSI vs ATN/IPS and ARINC429 fundamentals.
- Complete the software-only message flow.
- Write first 10 requirements and 10 tests.

## Weeks 3–4 — test automation and instrumentation
- Add pytest integration tests.
- Add JSONL logging and PCAP capture.
- Create KPI scripts for delivery ratio and latency.
- Publish v0.2 with a repeatable test campaign.

## Weeks 5–6 — communication bearer simulation
- Build Linux network namespaces.
- Add VDL2-like and SATCOM-like impaired links with netem.
- Demonstrate failover and failure recovery.
- Write root-cause analysis for an intentionally introduced defect.

## Weeks 7–8 — ARINC429 hardware-in-the-loop
- Build isolated loopback using RP2040/RP2350 proof-of-concept hardware or a commercial adapter.
- Generate/receive selected test labels.
- Add parity and unexpected-label negative tests.
- Photograph and document the bench.

## Weeks 9–10 — ATN/IPS-inspired IPv6
- Add FRRouting.
- Create aircraft, service-provider and ground IPv6 domains.
- Measure BGP route convergence after a link withdrawal.
- Add QoS / priority experiment.

## Week 11 — passive VDL2 observation
- Add receive-only SDR.
- Run dumpvdl2/libacars.
- Compare public/protocol observations with your simulator abstractions.
- Do not store/share sensitive message content unnecessarily.

## Week 12 — application package
- Run frozen v1.0 campaign.
- Produce final engineering report.
- Record demo video.
- Clean README and issue tracker.
- Add architecture and test evidence to CV/LinkedIn.

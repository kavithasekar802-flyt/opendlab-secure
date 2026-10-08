# Security & Assurance Test Plan

This workstream is intentionally designed around transferable network-security experience.

## Objectives

- prove that only documented communication paths are accepted
- detect configuration drift between test campaigns
- identify unintended listening services in the isolated home lab
- reject malformed or unauthorized datalink messages
- correlate security events with functional test behaviour
- produce an auditable engineering disposition

## Tests

| ID | Test | Existing skill leveraged | Expected evidence |
|---|---|---|---|
| SEC-001 | Approved source/destination path | firewall/whitelisting | allow event + PCAP |
| SEC-002 | Unauthorized source | least privilege | security_reject event |
| SEC-003 | Unauthorized service | port/service approval | rejection + reason |
| SEC-004 | Oversized/malformed payload | vulnerability mindset | safe rejection |
| SEC-005 | Unexpected open TCP/UDP service | Nmap | before/after inventory |
| SEC-006 | Configuration drift | exception/config discipline | SHA-256 drift result |
| SEC-007 | Bearer configuration changed without baseline update | audit control | campaign blocked |
| SEC-008 | Replay/duplicate message | anomaly analysis | duplicate identified |
| SEC-009 | Link degradation | network troubleshooting | packet/latency evidence |
| SEC-010 | Event-correlation exercise | SIEM mindset | single incident timeline |

## Nmap scope

Run Nmap only against machines/namespaces/devices owned by the project, for example:

```bash
nmap -sV 127.0.0.1
```

or an isolated RFC1918 home-lab namespace.

Never scan Airbus, airline, airport, aircraft, supplier or other systems without explicit
authorization.

## Engineering disposition template

- Observation
- Reproducibility
- Configuration / Git commit
- Functional impact
- Security impact
- Severity
- Evidence
- Probable cause
- Recommended correction
- Re-test required
- Final disposition

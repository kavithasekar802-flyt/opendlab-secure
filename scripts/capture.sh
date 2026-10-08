#!/usr/bin/env bash
set -euo pipefail
mkdir -p artifacts
IFACE="${1:-any}"
sudo tcpdump -i "$IFACE" -w artifacts/test_campaign.pcap

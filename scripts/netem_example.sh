#!/usr/bin/env bash
set -euo pipefail

# Apply to a disposable Linux test interface only.
# Example:
#   sudo ./scripts/netem_example.sh veth-vdl2 vdl2
#
# Remove:
#   sudo tc qdisc del dev veth-vdl2 root

IFACE="${1:-}"
PROFILE="${2:-}"

if [[ -z "$IFACE" || -z "$PROFILE" ]]; then
  echo "usage: $0 <interface> <vdl2|satcom|wifi>"
  exit 2
fi

sudo tc qdisc del dev "$IFACE" root 2>/dev/null || true

case "$PROFILE" in
  vdl2)
    sudo tc qdisc add dev "$IFACE" root netem \
      rate 31500bit delay 120ms 20ms loss 0.2% duplicate 0.02%
    ;;
  satcom)
    sudo tc qdisc add dev "$IFACE" root netem \
      rate 256kbit delay 300ms 80ms loss 0.1% reorder 0.02%
    ;;
  wifi)
    sudo tc qdisc add dev "$IFACE" root netem \
      delay 15ms 5ms loss 0.05%
    ;;
  *)
    echo "unknown profile: $PROFILE"
    exit 3
    ;;
esac

tc qdisc show dev "$IFACE"

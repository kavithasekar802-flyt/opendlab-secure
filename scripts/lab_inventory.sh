#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-127.0.0.1}"

case "$TARGET" in
  127.0.0.1|localhost|10.*|192.168.*|172.16.*|172.17.*|172.18.*|172.19.*|172.2?.*|172.30.*|172.31.*)
    ;;
  *)
    echo "Refusing non-private/non-local target. Use this helper only for your owned lab."
    exit 2
    ;;
esac

mkdir -p artifacts
nmap -sV "$TARGET" -oN artifacts/nmap_inventory.txt

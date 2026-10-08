from __future__ import annotations
import json
import socket
import time
from src.common import DatalinkMessage, event_id, utc_now

ROUTER_ADDR = ("127.0.0.1", 5000)

def build_message(seq: int) -> DatalinkMessage:
    service = "ATS" if seq % 3 == 0 else "AOC"
    priority = 1 if service == "ATS" else 5
    return DatalinkMessage(
        msg_id=event_id(),
        timestamp=utc_now(),
        source="ACFT_SIM",
        destination="GROUND_SIM",
        service=service,
        priority=priority,
        payload={
            "sequence": seq,
            "phase": "CRUISE",
            "text": "POSITION_REPORT" if service == "ATS" else "OPS_STATUS",
        },
    )

def main(count: int = 10, interval_s: float = 0.5):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for seq in range(1, count + 1):
        msg = build_message(seq)
        sock.sendto(json.dumps(msg.to_dict()).encode("utf-8"), ROUTER_ADDR)
        print(f"[AIRCRAFT] sent {msg.msg_id} {msg.service} prio={msg.priority}")
        time.sleep(interval_s)

if __name__ == "__main__":
    main()

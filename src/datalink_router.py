from __future__ import annotations
import asyncio
import json
import os
from src.common import append_jsonl, utc_now
from src.security_policy import authorize_message

AIRCRAFT_HOST = "127.0.0.1"
AIRCRAFT_PORT = 5000
GROUND_ADDR = ("127.0.0.1", 5100)

# Environment flags make failover demonstrable without changing code.
# Example: VDL2_HEALTH=0 python src/datalink_router.py
BEARERS = {
    "VDL2_SIM": {
        "healthy": os.getenv("VDL2_HEALTH", "1") == "1",
        "cost": 1,
        "nominal_latency_ms": 120,
    },
    "SATCOM_SIM": {
        "healthy": os.getenv("SATCOM_HEALTH", "1") == "1",
        "cost": 2,
        "nominal_latency_ms": 600,
    },
    "WIFI_LAB": {
        "healthy": os.getenv("WIFI_HEALTH", "1") == "1",
        "cost": 3,
        "nominal_latency_ms": 30,
    },
}

def choose_bearer(priority: int = 5) -> str:
    # Educational policy:
    # prefer the lowest-cost healthy bearer; for priority 0/1 prefer lowest latency.
    healthy = [(name, cfg) for name, cfg in BEARERS.items() if cfg["healthy"]]
    if not healthy:
        raise RuntimeError("no healthy bearer available")
    if priority <= 1:
        return min(healthy, key=lambda x: x[1]["nominal_latency_ms"])[0]
    return min(healthy, key=lambda x: x[1]["cost"])[0]

class RouterProtocol(asyncio.DatagramProtocol):
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        try:
            msg = json.loads(data.decode("utf-8"))
            allowed, reason = authorize_message(msg)
            if not allowed:
                append_jsonl("router_events.jsonl", {
                    "router_ts": utc_now(),
                    "event": "security_reject",
                    "reason": reason,
                    "source_addr": f"{addr[0]}:{addr[1]}",
                    "msg_id": msg.get("msg_id"),
                })
                print(f"[ROUTER] SECURITY REJECT {reason}")
                return
            bearer = choose_bearer(msg.get("priority", 5))
            envelope = {
                "router_ts": utc_now(),
                "bearer": bearer,
                "message": msg,
            }
            raw = json.dumps(envelope).encode("utf-8")
            self.transport.sendto(raw, GROUND_ADDR)
            append_jsonl("router_events.jsonl", {
                "event": "forward",
                "source_addr": f"{addr[0]}:{addr[1]}",
                **envelope,
            })
            print(f"[ROUTER] {msg.get('msg_id')} -> {bearer}")
        except Exception as exc:
            append_jsonl("router_events.jsonl", {
                "router_ts": utc_now(),
                "event": "router_error",
                "error": repr(exc),
            })
            print(f"[ROUTER] ERROR {exc}")

async def main():
    loop = asyncio.get_running_loop()
    transport, _ = await loop.create_datagram_endpoint(
        RouterProtocol, local_addr=(AIRCRAFT_HOST, AIRCRAFT_PORT)
    )
    print(f"[ROUTER] aircraft input udp://{AIRCRAFT_HOST}:{AIRCRAFT_PORT}")
    print(f"[ROUTER] bearer health: {BEARERS}")
    try:
        await asyncio.Future()
    finally:
        transport.close()

if __name__ == "__main__":
    asyncio.run(main())

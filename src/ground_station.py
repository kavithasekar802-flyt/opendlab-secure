from __future__ import annotations
import asyncio
import json
from src.common import append_jsonl, utc_now

HOST = "127.0.0.1"
PORT = 5100

class GroundProtocol(asyncio.DatagramProtocol):
    def datagram_received(self, data, addr):
        try:
            envelope = json.loads(data.decode("utf-8"))
            record = {
                "ts_ground": utc_now(),
                "event": "ground_rx",
                "from": f"{addr[0]}:{addr[1]}",
                **envelope,
            }
            append_jsonl("ground_events.jsonl", record)
            print(
                f"[GROUND] bearer={envelope.get('bearer')} "
                f"id={envelope.get('message', {}).get('msg_id')} "
                f"service={envelope.get('message', {}).get('service')}"
            )
        except Exception as exc:
            append_jsonl("ground_events.jsonl", {
                "ts_ground": utc_now(),
                "event": "ground_decode_error",
                "error": repr(exc),
            })

async def main():
    loop = asyncio.get_running_loop()
    transport, _ = await loop.create_datagram_endpoint(
        GroundProtocol, local_addr=(HOST, PORT)
    )
    print(f"[GROUND] listening on udp://{HOST}:{PORT}")
    try:
        await asyncio.Future()
    finally:
        transport.close()

if __name__ == "__main__":
    asyncio.run(main())

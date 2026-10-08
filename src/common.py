from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import json
import uuid

ARTIFACT_DIR = Path(__file__).resolve().parents[1] / "artifacts"
ARTIFACT_DIR.mkdir(exist_ok=True)

def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()

def event_id() -> str:
    return str(uuid.uuid4())

def append_jsonl(filename: str, record: dict) -> None:
    path = ARTIFACT_DIR / filename
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, separators=(",", ":")) + "\n")

@dataclass
class DatalinkMessage:
    msg_id: str
    timestamp: str
    source: str
    destination: str
    service: str
    priority: int
    payload: dict

    def to_dict(self) -> dict:
        return asdict(self)

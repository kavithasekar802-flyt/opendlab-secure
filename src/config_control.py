from __future__ import annotations
from hashlib import sha256
from pathlib import Path
import json

def file_sha256(path: str | Path) -> str:
    h = sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def make_manifest(paths: list[str | Path]) -> dict[str, str]:
    return {str(Path(p)): file_sha256(p) for p in paths}

def compare_manifest(expected: dict[str, str]) -> dict[str, str]:
    result = {}
    for filename, expected_hash in expected.items():
        path = Path(filename)
        if not path.exists():
            result[filename] = "MISSING"
        elif file_sha256(path) != expected_hash:
            result[filename] = "DRIFT"
        else:
            result[filename] = "OK"
    return result

def save_manifest(manifest: dict[str, str], output: str | Path) -> None:
    Path(output).write_text(json.dumps(manifest, indent=2), encoding="utf-8")

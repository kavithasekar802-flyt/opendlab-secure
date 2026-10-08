from __future__ import annotations

ALLOWED_SOURCES = {"ACFT_SIM"}
ALLOWED_DESTINATIONS = {"GROUND_SIM"}
ALLOWED_SERVICES = {"ATS", "ABC", "MAINT"}
MAX_PAYLOAD_BYTES = 2048

def authorize_message(msg: dict) -> tuple[bool, str]:
    """
    Educational application-layer policy gate inspired by least-privilege,
    source/destination whitelisting and documented network-change controls.
    """
    required = {"msg_id", "source", "destination", "service", "priority", "payload"}
    missing = required.difference(msg)
    if missing:
        return False, f"missing_fields:{','.join(sorted(missing))}"

    if msg["source"] not in ALLOWED_SOURCES:
        return False, "source_not_whitelisted"

    if msg["destination"] not in ALLOWED_DESTINATIONS:
        return False, "destination_not_whitelisted"

    if msg["service"] not in ALLOWED_SERVICES:
        return False, "service_not_authorized"

    payload_size = len(str(msg["payload"]).encode("utf-8"))
    if payload_size > MAX_PAYLOAD_BYTES:
        return False, "payload_too_large"

    try:
        priority = int(msg["priority"])
    except (TypeError, ValueError):
        return False, "invalid_priority"

    if not 0 <= priority <= 9:
        return False, "priority_out_of_range"

    return True, "authorized"

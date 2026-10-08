from src.security_policy import authorize_message

def valid_message():
    return {
        "msg_id": "T-1",
        "source": "ACFT_SIM",
        "destination": "GROUND_SIM",
        "service": "ATS",
        "priority": 1,
        "payload": {"text": "TEST"},
    }

def test_authorized_nominal_message():
    ok, reason = authorize_message(valid_message())
    assert ok is True
    assert reason == "authorized"

def test_reject_unknown_source():
    msg = valid_message()
    msg["source"] = "UNKNOWN_NODE"
    ok, reason = authorize_message(msg)
    assert ok is False
    assert reason == "source_not_whitelisted"

def test_reject_unauthorized_service():
    msg = valid_message()
    msg["service"] = "DEBUG_ADMIN"
    ok, reason = authorize_message(msg)
    assert ok is False
    assert reason == "service_not_authorized"

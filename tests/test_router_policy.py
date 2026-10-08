import src.datalink_router as router

def test_normal_policy_prefers_vdl2(monkeypatch):
    monkeypatch.setitem(router.BEARERS["VDL2_SIM"], "healthy", True)
    monkeypatch.setitem(router.BEARERS["SATCOM_SIM"], "healthy", True)
    monkeypatch.setitem(router.BEARERS["WIFI_LAB"], "healthy", True)
    assert router.choose_bearer(priority=5) == "VDL2_SIM"

def test_failover_to_satcom(monkeypatch):
    monkeypatch.setitem(router.BEARERS["VDL2_SIM"], "healthy", False)
    monkeypatch.setitem(router.BEARERS["SATCOM_SIM"], "healthy", True)
    monkeypatch.setitem(router.BEARERS["WIFI_LAB"], "healthy", True)
    assert router.choose_bearer(priority=5) == "SATCOM_SIM"

def test_priority_prefers_low_latency(monkeypatch):
    for cfg in router.BEARERS.values():
        monkeypatch.setitem(cfg, "healthy", True)
    assert router.choose_bearer(priority=1) == "WIFI_LAB"

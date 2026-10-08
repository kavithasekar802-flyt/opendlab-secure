from src.config_control import make_manifest, compare_manifest

def test_detect_configuration_drift(tmp_path):
    f = tmp_path / "bearer.cfg"
    f.write_text("latency=120", encoding="utf-8")
    baseline = make_manifest([f])
    assert compare_manifest(baseline)[str(f)] == "OK"
    f.write_text("latency=999", encoding="utf-8")
    assert compare_manifest(baseline)[str(f)] == "DRIFT"

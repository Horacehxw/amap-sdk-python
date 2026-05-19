from pathlib import Path


def test_integration_policy_requires_live_opt_in():
    conftest = Path(__file__).with_name("conftest.py").read_text()
    integration = Path(__file__).with_name("test_integration.py").read_text()

    assert "AMAP_LIVE" in conftest
    assert "AMAP_LIVE=1" in integration


def test_sdk_src_has_no_shanshichuan_business_rules():
    src_root = Path(__file__).resolve().parents[1] / "src"
    text = "\n".join(path.read_text(encoding="utf-8") for path in src_root.rglob("*.py"))

    assert "山似川" not in text
    assert "大竹林" not in text
    assert "人和店" not in text
    assert "光环店" not in text

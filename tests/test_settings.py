import json, pathlib, pytest
from src.settings import Settings

DEFAULTS = pathlib.Path("config/default_settings.json")

def test_loads_defaults(tmp_path):
    s = Settings(config_path=tmp_path / "s.json", defaults_path=DEFAULTS)
    assert s.get("socket_port") == 47291

def test_saves_and_reloads(tmp_path):
    p = tmp_path / "s.json"
    s = Settings(config_path=p, defaults_path=DEFAULTS)
    s.set("muted", True)
    s.save()
    s2 = Settings(config_path=p, defaults_path=DEFAULTS)
    assert s2.get("muted") is True

def test_unknown_key_returns_none(tmp_path):
    s = Settings(config_path=tmp_path / "s.json", defaults_path=DEFAULTS)
    assert s.get("nonexistent_key") is None

def test_get_all_merges_over_defaults(tmp_path):
    s = Settings(config_path=tmp_path / "s.json", defaults_path=DEFAULTS)
    s.set("muted", True)
    all_s = s.get_all()
    assert all_s["muted"] is True
    assert all_s["socket_port"] == 47291

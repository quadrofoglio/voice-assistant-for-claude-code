import json, pathlib

def test_default_settings_valid():
    path = pathlib.Path("config/default_settings.json")
    data = json.loads(path.read_text())
    assert "stt_hotkey" in data
    assert "socket_port" in data
    assert data["socket_port"] == 47291
    assert data["whisper_model"] == "small"

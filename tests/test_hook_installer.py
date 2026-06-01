import json, pathlib, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import src.hook_installer as hi

def test_installs_hook(tmp_path):
    settings_path = tmp_path / "settings.json"
    settings_path.write_text("{}")
    hook_dir = tmp_path / "hooks"
    orig = hi.CLAUDE_SETTINGS_PATH
    hi.CLAUDE_SETTINGS_PATH = settings_path
    try:
        hi.install_hook(hook_dest_dir=hook_dir)
        data = json.loads(settings_path.read_text())
        assert any("voice_assistant_stop_hook" in h["command"] for h in data["hooks"])
    finally:
        hi.CLAUDE_SETTINGS_PATH = orig

def test_no_duplicate_hook(tmp_path):
    settings_path = tmp_path / "settings.json"
    settings_path.write_text("{}")
    hook_dir = tmp_path / "hooks"
    orig = hi.CLAUDE_SETTINGS_PATH
    hi.CLAUDE_SETTINGS_PATH = settings_path
    try:
        hi.install_hook(hook_dest_dir=hook_dir)
        hi.install_hook(hook_dest_dir=hook_dir)
        data = json.loads(settings_path.read_text())
        count = sum(1 for h in data["hooks"] if "voice_assistant_stop_hook" in h["command"])
        assert count == 1
    finally:
        hi.CLAUDE_SETTINGS_PATH = orig

import json
import pathlib
import shutil
import sys
from src.paths import bundle_dir

CLAUDE_SETTINGS_PATH = pathlib.Path.home() / ".claude" / "settings.json"
HOOK_SCRIPT_SRC = bundle_dir() / "hook" / "stop_hook.py"

def install_hook(hook_dest_dir: pathlib.Path = None) -> None:
    hook_dest_dir = hook_dest_dir or pathlib.Path.home() / ".claude" / "hooks"
    hook_dest_dir.mkdir(parents=True, exist_ok=True)

    hook_dest = hook_dest_dir / "voice_assistant_stop_hook.py"
    shutil.copy(HOOK_SCRIPT_SRC, hook_dest)

    hook_cmd = f'"{sys.executable}" "{hook_dest}"'

    settings: dict = {}
    if CLAUDE_SETTINGS_PATH.exists():
        settings = json.loads(CLAUDE_SETTINGS_PATH.read_text())

    hooks = settings.setdefault("hooks", [])
    hooks[:] = [h for h in hooks if "voice_assistant_stop_hook" not in h.get("command", "")]
    hooks.append({"event": "Stop", "command": hook_cmd})

    CLAUDE_SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    CLAUDE_SETTINGS_PATH.write_text(json.dumps(settings, indent=2))

def is_hook_installed() -> bool:
    if not CLAUDE_SETTINGS_PATH.exists():
        return False
    settings = json.loads(CLAUDE_SETTINGS_PATH.read_text())
    return any("voice_assistant_stop_hook" in h.get("command", "") for h in settings.get("hooks", []))

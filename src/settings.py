import json
import pathlib
from typing import Any
from src.paths import bundle_dir


class Settings:
    def __init__(self, config_path: pathlib.Path = None, defaults_path: pathlib.Path = None):
        self._defaults_path = defaults_path or bundle_dir() / "config" / "default_settings.json"
        self._config_path = config_path or pathlib.Path.home() / ".voice_assistant" / "settings.json"
        self._config_path.parent.mkdir(parents=True, exist_ok=True)
        self._defaults = json.loads(self._defaults_path.read_text())
        self._data: dict = {}
        if self._config_path.exists():
            self._data = json.loads(self._config_path.read_text())

    def get(self, key: str) -> Any:
        return self._data.get(key, self._defaults.get(key))

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def save(self) -> None:
        self._config_path.write_text(json.dumps(self._data, indent=2))

    def get_all(self) -> dict:
        return {**self._defaults, **self._data}

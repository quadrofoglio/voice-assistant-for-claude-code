import pathlib
from unittest.mock import MagicMock, patch
from src.settings import Settings
from src.tts import TTSOrchestrator

DEFAULTS = pathlib.Path("config/default_settings.json")

def make_settings(tmp_path):
    return Settings(config_path=tmp_path / "s.json", defaults_path=DEFAULTS)

def test_muted_does_not_speak(tmp_path):
    s = make_settings(tmp_path)
    s.set("muted", True)
    tts = TTSOrchestrator(s)
    tts._edge = MagicMock()
    tts._piper = MagicMock()
    tts.speak("hello")
    tts._edge.speak.assert_not_called()
    tts._piper.speak.assert_not_called()

def test_store_last_cleans_text(tmp_path):
    s = make_settings(tmp_path)
    tts = TTSOrchestrator(s)
    tts.store_last("```python\ndef foo(): pass\n```\nHello world")
    assert "def foo" not in tts._last_text
    assert "Hello world" in tts._last_text

def test_set_muted_updates_settings(tmp_path):
    s = make_settings(tmp_path)
    tts = TTSOrchestrator(s)
    tts.set_muted(True)
    assert s.get("muted") is True

def test_speak_last_empty_does_nothing(tmp_path):
    s = make_settings(tmp_path)
    tts = TTSOrchestrator(s)
    tts._edge = MagicMock()
    tts._last_text = ""
    tts.speak_last()
    tts._edge.speak.assert_not_called()

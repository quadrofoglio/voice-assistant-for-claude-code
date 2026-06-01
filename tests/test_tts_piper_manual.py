import pytest
from src.tts_piper import PiperTTS
from src.piper_manager import is_downloaded, AVAILABLE_VOICES


def test_available_voices_dict_has_entries():
    assert len(AVAILABLE_VOICES) >= 5
    assert "en_US-amy-medium" in AVAILABLE_VOICES


def test_piper_tts_unavailable_when_no_exe_or_voice(tmp_path, monkeypatch):
    import src.tts_piper as tp
    monkeypatch.setattr(tp, "PIPER_EXE", None)
    tts = PiperTTS("en_US-amy-medium")
    assert tts.is_available() is False


@pytest.mark.skip(reason="manual test — requires speakers, piper.exe, and voice files")
def test_speaks_text():
    tts = PiperTTS("en_US-amy-medium")
    assert tts.is_available(), "Run scripts/download_piper.py and download voice first"
    tts.speak("Piper TTS offline voice is working.")

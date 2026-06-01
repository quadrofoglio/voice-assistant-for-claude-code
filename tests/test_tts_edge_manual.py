import pytest
from src.tts_edge import EdgeTTS

@pytest.mark.skip(reason="manual test — requires speakers and internet")
def test_speaks_text():
    tts = EdgeTTS(voice="en-US-AriaNeural")
    tts.speak("Edge TTS is working correctly.")

def test_list_voices_returns_8_entries():
    voices = EdgeTTS.list_voices()
    assert len(voices) == 8
    assert "en-US-AriaNeural" in voices

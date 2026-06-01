import pytest, time, pathlib
from src.stt import STT
from src.settings import Settings

@pytest.mark.skip(reason="manual test — requires microphone")
def test_transcribes_speech():
    settings = Settings(defaults_path=pathlib.Path("config/default_settings.json"))
    stt = STT(settings)
    print("\nSpeak now for 3 seconds...")
    stt.start_recording()
    time.sleep(3)
    result = stt.stop_recording()
    print(f"Transcribed: '{result}'")
    assert len(result) > 0

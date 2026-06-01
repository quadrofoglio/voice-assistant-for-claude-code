import asyncio
import tempfile
import os
import edge_tts

class EdgeTTS:
    CURATED_VOICES = [
        "en-US-AriaNeural",
        "en-US-GuyNeural",
        "en-US-JennyNeural",
        "en-GB-SoniaNeural",
        "en-GB-RyanNeural",
        "en-AU-NatashaNeural",
        "en-AU-WilliamNeural",
        "en-IN-NeerjaNeural",
    ]

    def __init__(self, voice: str = "en-US-AriaNeural"):
        self._voice = voice

    def set_voice(self, voice: str) -> None:
        self._voice = voice

    def speak(self, text: str) -> None:
        asyncio.run(self._speak_async(text))

    async def _speak_async(self, text: str) -> None:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            tmp_path = f.name
        communicate = edge_tts.Communicate(text, self._voice)
        await communicate.save(tmp_path)
        os.startfile(tmp_path)

    @staticmethod
    def list_voices() -> list:
        return EdgeTTS.CURATED_VOICES

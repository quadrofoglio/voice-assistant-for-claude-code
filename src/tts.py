from src.tts_edge import EdgeTTS
from src.tts_piper import PiperTTS
from src.text_cleaner import clean_for_tts
from src.settings import Settings

class TTSOrchestrator:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._edge = EdgeTTS(voice=settings.get("edge_voice"))
        self._piper = PiperTTS(voice_name=settings.get("piper_voice"))
        self._last_text = ""

    def speak(self, text: str) -> None:
        if self._settings.get("muted"):
            return
        cleaned = clean_for_tts(text)
        if not cleaned.strip():
            return
        self._last_text = cleaned
        engine = self._settings.get("tts_engine")
        if engine == "piper" and self._piper.is_available():
            self._piper.speak(cleaned)
        else:
            try:
                self._edge.speak(cleaned)
            except Exception:
                if self._piper.is_available():
                    self._piper.speak(cleaned)

    def speak_last(self) -> None:
        if self._last_text:
            self.speak(self._last_text)

    def set_muted(self, muted: bool) -> None:
        self._settings.set("muted", muted)

    def store_last(self, text: str) -> None:
        self._last_text = clean_for_tts(text)

    def update_voice(self, engine: str, voice: str) -> None:
        self._settings.set("tts_engine", engine)
        if engine == "edge":
            self._settings.set("edge_voice", voice)
            self._edge.set_voice(voice)
        elif engine == "piper":
            self._settings.set("piper_voice", voice)
            self._piper.set_voice(voice)

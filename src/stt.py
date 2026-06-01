import numpy as np
import sounddevice as sd
import threading
from faster_whisper import WhisperModel
from src.settings import Settings

SAMPLE_RATE = 16000

class STT:
    def __init__(self, settings: Settings):
        model_size = settings.get("whisper_model") or "small"
        self._model = WhisperModel(model_size, device="cpu", compute_type="int8")
        self._recording = False
        self._frames: list = []
        self._lock = threading.Lock()
        self._stream = None

    def start_recording(self) -> None:
        with self._lock:
            self._frames = []
            self._recording = True
        self._stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            callback=self._audio_callback,
        )
        self._stream.start()

    def stop_recording(self) -> str:
        self._recording = False
        if self._stream:
            self._stream.stop()
            self._stream.close()
        with self._lock:
            if not self._frames:
                return ""
            audio = np.concatenate(self._frames, axis=0).flatten()
        segments, _ = self._model.transcribe(audio, beam_size=5, language="en")
        return " ".join(s.text.strip() for s in segments).strip()

    def _audio_callback(self, indata, frames, time, status) -> None:
        if self._recording:
            with self._lock:
                self._frames.append(indata.copy())

import pathlib
import subprocess
import tempfile
import os
from src.paths import exe_dir

VOICES_DIR = exe_dir() / "voices"
PIPER_EXE = next(exe_dir().joinpath("piper_bin").rglob("piper.exe"), None) if exe_dir().joinpath("piper_bin").exists() else None


class PiperTTS:
    def __init__(self, voice_name: str = "en_US-amy-medium"):
        self._voice_name = voice_name

    def set_voice(self, voice_name: str) -> None:
        self._voice_name = voice_name

    def is_available(self) -> bool:
        if not PIPER_EXE or not PIPER_EXE.exists():
            return False
        model = VOICES_DIR / f"{self._voice_name}.onnx"
        return model.exists()

    def speak(self, text: str) -> None:
        if not self.is_available():
            raise RuntimeError(
                f"Piper not available. Run scripts/download_piper.py and download voices."
            )
        model = VOICES_DIR / f"{self._voice_name}.onnx"
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            tmp_path = f.name
        subprocess.run(
            [str(PIPER_EXE), "--model", str(model), "--output_file", tmp_path],
            input=text.encode(),
            check=True,
            capture_output=True,
        )
        os.startfile(tmp_path)

    @property
    def voice_name(self) -> str:
        return self._voice_name

    @staticmethod
    def list_downloaded() -> list:
        return [p.stem for p in VOICES_DIR.glob("*.onnx")]

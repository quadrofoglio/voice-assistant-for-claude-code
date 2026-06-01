import pathlib
import urllib.request
from typing import Callable
from src.paths import exe_dir

VOICES_DIR = exe_dir() / "voices"
HF_BASE = "https://huggingface.co/rhasspy/piper-voices/resolve/main"

AVAILABLE_VOICES = {
    "en_US-amy-medium":         "en/en_US/amy/medium",
    "en_US-lessac-medium":      "en/en_US/lessac/medium",
    "en_US-ryan-medium":        "en/en_US/ryan/medium",
    "en_GB-alan-medium":        "en/en_GB/alan/medium",
    "en_GB-jenny_dioco-medium": "en/en_GB/jenny_dioco/medium",
}


def download_voice(voice_name: str, progress_cb: Callable[[int], None] = None) -> None:
    if voice_name not in AVAILABLE_VOICES:
        raise ValueError(f"Unknown voice: {voice_name}")
    VOICES_DIR.mkdir(exist_ok=True)
    prefix = AVAILABLE_VOICES[voice_name]
    for i, ext in enumerate((".onnx", ".onnx.json")):
        url = f"{HF_BASE}/{prefix}/{voice_name}{ext}"
        dest = VOICES_DIR / f"{voice_name}{ext}"
        if not dest.exists():
            urllib.request.urlretrieve(url, dest)
        if progress_cb:
            progress_cb(50 * (i + 1))


def is_downloaded(voice_name: str) -> bool:
    return (VOICES_DIR / f"{voice_name}.onnx").exists()

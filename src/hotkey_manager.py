import threading
import keyboard
from typing import Callable


class HotkeyManager:
    def __init__(self):
        self._stt_hotkey: str = ""
        self._on_start: Callable = None
        self._on_stop: Callable = None
        self._tts_hotkey: str = ""
        self._tts_callback: Callable = None
        self._recording: bool = False

    def register_ptt(self, hotkey: str, on_start: Callable, on_stop: Callable) -> None:
        self._stt_hotkey = hotkey
        self._on_start = on_start
        self._on_stop = on_stop

    def register_hotkey(self, hotkey: str, callback: Callable) -> None:
        self._tts_hotkey = hotkey
        self._tts_callback = callback

    def start(self) -> None:
        if self._stt_hotkey and self._on_start:
            keyboard.add_hotkey(self._stt_hotkey, self._toggle_recording, suppress=True)
        if self._tts_hotkey and self._tts_callback:
            keyboard.add_hotkey(self._tts_hotkey, self._tts_callback)

    def stop(self) -> None:
        try:
            keyboard.unhook_all_hotkeys()
        except Exception:
            pass
        self._recording = False

    def update_ptt(self, new_hotkey: str) -> None:
        self.stop()
        self._stt_hotkey = new_hotkey
        self.start()

    def update_tts_hotkey(self, new_hotkey: str) -> None:
        self.stop()
        self._tts_hotkey = new_hotkey
        self.start()

    def _toggle_recording(self) -> None:
        if not self._recording:
            self._recording = True
            if self._on_start:
                threading.Thread(target=self._on_start, daemon=True).start()
        else:
            self._recording = False
            if self._on_stop:
                threading.Thread(target=self._on_stop, daemon=True).start()

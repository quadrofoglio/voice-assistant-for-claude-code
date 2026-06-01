import threading
import keyboard
from typing import Callable

class HotkeyManager:
    def __init__(self):
        self._ptt_hotkey: str = ""
        self._ptt_on_start: Callable = None
        self._ptt_on_stop: Callable = None
        self._tts_hotkey: str = ""
        self._tts_callback: Callable = None
        self._ptt_active: bool = False
        self._hooks: list = []

    def register_ptt(self, hotkey: str, on_start: Callable, on_stop: Callable) -> None:
        self._ptt_hotkey = hotkey
        self._ptt_on_start = on_start
        self._ptt_on_stop = on_stop

    def register_hotkey(self, hotkey: str, callback: Callable) -> None:
        self._tts_hotkey = hotkey
        self._tts_callback = callback

    def start(self) -> None:
        self._hooks.append(keyboard.on_press(self._on_press))
        self._hooks.append(keyboard.on_release(self._on_release))
        if self._tts_hotkey and self._tts_callback:
            keyboard.add_hotkey(self._tts_hotkey, self._tts_callback)

    def stop(self) -> None:
        for hook in self._hooks:
            keyboard.unhook(hook)
        self._hooks.clear()
        if self._tts_hotkey:
            try:
                keyboard.remove_hotkey(self._tts_hotkey)
            except Exception:
                pass

    def update_ptt(self, new_hotkey: str) -> None:
        self._ptt_hotkey = new_hotkey

    def update_tts_hotkey(self, new_hotkey: str) -> None:
        self.stop()
        self._tts_hotkey = new_hotkey
        self.start()

    def _on_press(self, event: keyboard.KeyboardEvent) -> None:
        if not self._ptt_active and self._ptt_hotkey and keyboard.is_pressed(self._ptt_hotkey):
            self._ptt_active = True
            if self._ptt_on_start:
                threading.Thread(target=self._ptt_on_start, daemon=True).start()

    def _on_release(self, event: keyboard.KeyboardEvent) -> None:
        if self._ptt_active and self._ptt_hotkey:
            main_key = self._ptt_hotkey.split("+")[-1].strip()
            if event.name == main_key:
                self._ptt_active = False
                if self._ptt_on_stop:
                    threading.Thread(target=self._ptt_on_stop, daemon=True).start()

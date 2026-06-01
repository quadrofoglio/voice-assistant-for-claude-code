import pystray
from PIL import Image
import pathlib
import threading
from typing import Callable

class AppTray:
    def __init__(self, on_open: Callable, on_quit: Callable, on_mute_toggle: Callable):
        self._on_open = on_open
        self._on_quit = on_quit
        self._on_mute_toggle = on_mute_toggle
        self._icon = None
        self._muted = False

    def start(self) -> None:
        image = Image.open(pathlib.Path("assets/icon.png"))
        menu = pystray.Menu(
            pystray.MenuItem("Open", self._on_open, default=True),
            pystray.MenuItem("Mute TTS", self._toggle_mute, checked=lambda item: self._muted),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Quit", self._quit),
        )
        self._icon = pystray.Icon("VoiceAssistant", image, "Voice Assistant", menu)
        self._icon.run()

    def _toggle_mute(self) -> None:
        self._muted = not self._muted
        self._on_mute_toggle(self._muted)

    def _quit(self) -> None:
        self._icon.stop()
        self._on_quit()

    def set_status(self, status: str) -> None:
        if self._icon:
            self._icon.title = f"Voice Assistant — {status}"

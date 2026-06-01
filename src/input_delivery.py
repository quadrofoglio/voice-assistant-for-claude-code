import pyperclip
from pynput.keyboard import Controller

class InputDelivery:
    def __init__(self, mode: str = "terminal"):
        self._mode = mode
        self._kb = Controller()

    @property
    def mode(self) -> str:
        return self._mode

    def set_mode(self, mode: str) -> None:
        if mode not in ("terminal", "clipboard"):
            raise ValueError(f"Unknown mode: {mode}")
        self._mode = mode

    def deliver(self, text: str) -> None:
        if self._mode == "clipboard":
            pyperclip.copy(text)
        else:
            self._kb.type(text)

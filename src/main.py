import threading
from src.settings import Settings
from src.socket_server import SocketServer
from src.stt import STT
from src.tts import TTSOrchestrator
from src.input_delivery import InputDelivery
from src.hotkey_manager import HotkeyManager
from src.preview import TranscriptionPreview
from src.tray import AppTray
from src.window import MainWindow
from src.settings_panel import SettingsPanel
from src.hook_installer import install_hook, is_hook_installed

class App:
    def __init__(self):
        self._settings = Settings()
        if not is_hook_installed():
            install_hook()
        self._stt = STT(self._settings)
        self._tts = TTSOrchestrator(self._settings)
        self._delivery = InputDelivery(mode=self._settings.get("input_mode"))
        self._hotkeys = HotkeyManager()
        self._window = MainWindow(
            on_open_settings=self._open_settings,
            on_tts_play=self._tts.speak_last,
            on_mute_toggle=self._tts.set_muted,
        )
        self._tray = AppTray(
            on_open=self._window.show,
            on_quit=self._quit,
            on_mute_toggle=self._tts.set_muted,
        )
        self._server = SocketServer(
            port=self._settings.get("socket_port"),
            on_message=self._on_hook_message,
        )

    def _on_hook_message(self, msg: dict) -> None:
        text = msg.get("text", "")
        if not text:
            return
        if self._settings.get("auto_play_tts"):
            threading.Thread(target=self._tts.speak, args=(text,), daemon=True).start()
        else:
            self._tts.store_last(text)

    def _on_stt_start(self) -> None:
        self._window.set_status("Recording...")
        self._tray.set_status("Recording")
        self._stt.start_recording()

    def _on_stt_stop(self) -> None:
        self._window.set_status("Transcribing...")
        self._tray.set_status("Transcribing")
        text = self._stt.stop_recording()
        self._window.set_status("Idle")
        self._tray.set_status("Idle")
        if not text:
            return
        self._window.set_transcript(text)
        TranscriptionPreview(
            timeout_seconds=self._settings.get("preview_timeout_seconds"),
            on_confirm=self._deliver,
            on_cancel=lambda: None,
        ).show(text)

    def _deliver(self, text: str) -> None:
        self._delivery.set_mode(self._settings.get("input_mode"))
        self._delivery.deliver(text)

    def _open_settings(self) -> None:
        SettingsPanel(self._settings, on_save=self._on_settings_saved).show()

    def _on_settings_saved(self) -> None:
        self._delivery.set_mode(self._settings.get("input_mode"))
        self._hotkeys.stop()
        self._register_hotkeys()
        self._hotkeys.start()

    def _register_hotkeys(self) -> None:
        self._hotkeys.register_ptt(
            hotkey=self._settings.get("stt_hotkey"),
            on_start=self._on_stt_start,
            on_stop=self._on_stt_stop,
        )
        self._hotkeys.register_hotkey(
            hotkey=self._settings.get("tts_hotkey"),
            callback=self._tts.speak_last,
        )

    def _quit(self) -> None:
        self._hotkeys.stop()
        self._server.stop()

    def run(self) -> None:
        threading.Thread(target=self._server.start, daemon=True).start()
        self._register_hotkeys()
        self._hotkeys.start()
        self._window.show()
        threading.Thread(target=self._tray.start, daemon=True).start()
        self._window.mainloop()

def main():
    App().run()

if __name__ == "__main__":
    main()

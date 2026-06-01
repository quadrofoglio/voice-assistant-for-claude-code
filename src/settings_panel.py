import tkinter as tk
from tkinter import ttk, messagebox
import threading
from src.settings import Settings
from src.piper_manager import AVAILABLE_VOICES, download_voice, is_downloaded
from src.tts_edge import EdgeTTS

class SettingsPanel:
    def __init__(self, settings: Settings, on_save: callable = None):
        self._settings = settings
        self._on_save = on_save

    def show(self) -> None:
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self) -> None:
        root = tk.Tk()
        root.title("Voice Assistant — Settings")
        root.geometry("520x600")
        root.resizable(False, False)
        root.attributes("-topmost", True)

        nb = ttk.Notebook(root)
        nb.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self._build_input_tab(nb)
        self._build_tts_tab(nb)
        self._build_guide_tab(nb)

        tk.Button(root, text="Save", command=lambda: self._save(root),
                  bg="#0078d4", fg="white", width=12).pack(pady=8)
        root.mainloop()

    def _build_input_tab(self, nb: ttk.Notebook) -> None:
        f = ttk.Frame(nb)
        nb.add(f, text="Input (STT)")

        tk.Label(f, text="Push-to-talk hotkey:").grid(row=0, column=0, sticky="w", padx=10, pady=8)
        self._stt_hk = tk.StringVar(value=self._settings.get("stt_hotkey"))
        tk.Entry(f, textvariable=self._stt_hk, width=20).grid(row=0, column=1, padx=10)

        tk.Label(f, text="Input mode:").grid(row=1, column=0, sticky="w", padx=10, pady=8)
        self._input_mode = tk.StringVar(value=self._settings.get("input_mode"))
        ttk.Combobox(f, textvariable=self._input_mode, values=["terminal", "clipboard"],
                     state="readonly", width=17).grid(row=1, column=1, padx=10)

        self._wake_enabled = tk.BooleanVar(value=self._settings.get("wake_word_enabled"))
        tk.Checkbutton(f, text="Enable wake word", variable=self._wake_enabled).grid(
            row=2, column=0, columnspan=2, sticky="w", padx=10, pady=8)

        tk.Label(f, text="Wake word:").grid(row=3, column=0, sticky="w", padx=10)
        self._wake_word = tk.StringVar(value=self._settings.get("wake_word"))
        tk.Entry(f, textvariable=self._wake_word, width=20).grid(row=3, column=1, padx=10)

        tk.Label(f, text="Whisper model:").grid(row=4, column=0, sticky="w", padx=10, pady=8)
        self._whisper_model = tk.StringVar(value=self._settings.get("whisper_model"))
        ttk.Combobox(f, textvariable=self._whisper_model,
                     values=["tiny", "base", "small", "medium"], state="readonly", width=17).grid(
            row=4, column=1, padx=10)

    def _build_tts_tab(self, nb: ttk.Notebook) -> None:
        f = ttk.Frame(nb)
        nb.add(f, text="Output (TTS)")

        tk.Label(f, text="TTS hotkey (on-demand):").grid(row=0, column=0, sticky="w", padx=10, pady=8)
        self._tts_hk = tk.StringVar(value=self._settings.get("tts_hotkey"))
        tk.Entry(f, textvariable=self._tts_hk, width=20).grid(row=0, column=1, padx=10)

        self._auto_play = tk.BooleanVar(value=self._settings.get("auto_play_tts"))
        tk.Checkbutton(f, text="Auto-play TTS when Claude responds",
                       variable=self._auto_play).grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=4)

        tk.Label(f, text="TTS engine:").grid(row=2, column=0, sticky="w", padx=10, pady=8)
        self._engine = tk.StringVar(value=self._settings.get("tts_engine"))
        ttk.Combobox(f, textvariable=self._engine, values=["edge", "piper"],
                     state="readonly", width=17).grid(row=2, column=1, padx=10)

        tk.Label(f, text="Edge voice:").grid(row=3, column=0, sticky="w", padx=10, pady=8)
        self._edge_voice = tk.StringVar(value=self._settings.get("edge_voice"))
        ttk.Combobox(f, textvariable=self._edge_voice, values=EdgeTTS.list_voices(),
                     state="readonly", width=28).grid(row=3, column=1, padx=10)

        tk.Label(f, text="Piper voice:").grid(row=4, column=0, sticky="w", padx=10, pady=8)
        self._piper_voice = tk.StringVar(value=self._settings.get("piper_voice"))
        ttk.Combobox(f, textvariable=self._piper_voice, values=list(AVAILABLE_VOICES.keys()),
                     state="readonly", width=28).grid(row=4, column=1, padx=10)

        tk.Button(f, text="Download selected Piper voice",
                  command=self._download_piper).grid(row=5, column=0, columnspan=2, padx=10, pady=8)

    def _build_guide_tab(self, nb: ttk.Notebook) -> None:
        f = ttk.Frame(nb)
        nb.add(f, text="How to Use")
        guide = (
            "SPEAKING TO CLAUDE\n"
            "  Hold your STT hotkey (default: alt+space)\n"
            "  Speak your message, then release the hotkey\n"
            "  A preview appears — auto-sends in 2 seconds\n"
            "  Click Send to confirm or Cancel to discard\n\n"
            "HEARING CLAUDE'S RESPONSE\n"
            "  Press TTS hotkey (default: alt+r) to read the last response\n"
            "  Enable Auto-play in Output tab to hear responses automatically\n\n"
            "HOTKEY FORMAT  (keyboard library syntax)\n"
            "  alt+space  ctrl+r  shift+f1  windows+v\n\n"
            "INPUT MODES\n"
            "  terminal  — auto-types into your active terminal window\n"
            "  clipboard — copies to clipboard; paste with Ctrl+V\n\n"
            "WAKE WORD\n"
            "  Enable in Input tab and set your trigger phrase\n"
            "  Say the phrase to start recording without holding a key\n\n"
            "TTS ENGINES\n"
            "  edge  — online, Microsoft neural voices, best quality\n"
            "  piper — offline, neural quality, works without internet\n"
        )
        txt = tk.Text(f, wrap=tk.WORD, width=58, height=24, font=("Segoe UI", 9))
        txt.insert(tk.END, guide)
        txt.config(state=tk.DISABLED)
        txt.pack(padx=10, pady=10)

    def _download_piper(self) -> None:
        voice = self._piper_voice.get()
        if is_downloaded(voice):
            messagebox.showinfo("Piper", f"{voice} is already downloaded.")
            return
        try:
            download_voice(voice)
            messagebox.showinfo("Piper", f"{voice} downloaded successfully.")
        except Exception as e:
            messagebox.showerror("Download Error", str(e))

    def _save(self, root: tk.Tk) -> None:
        self._settings.set("stt_hotkey", self._stt_hk.get())
        self._settings.set("tts_hotkey", self._tts_hk.get())
        self._settings.set("input_mode", self._input_mode.get())
        self._settings.set("wake_word_enabled", self._wake_enabled.get())
        self._settings.set("wake_word", self._wake_word.get())
        self._settings.set("whisper_model", self._whisper_model.get())
        self._settings.set("tts_engine", self._engine.get())
        self._settings.set("edge_voice", self._edge_voice.get())
        self._settings.set("piper_voice", self._piper_voice.get())
        self._settings.set("auto_play_tts", self._auto_play.get())
        self._settings.save()
        root.destroy()
        if self._on_save:
            self._on_save()

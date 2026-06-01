import tkinter as tk
from typing import Callable

class MainWindow:
    def __init__(self, on_open_settings: Callable, on_tts_play: Callable, on_mute_toggle: Callable):
        self._on_open_settings = on_open_settings
        self._on_tts_play = on_tts_play
        self._on_mute_toggle = on_mute_toggle
        self._root = None
        self._status_var = None
        self._transcript_var = None

    def show(self) -> None:
        if self._root:
            try:
                self._root.deiconify()
                self._root.lift()
                return
            except tk.TclError:
                pass
        self._root = tk.Tk()
        self._root.title("Voice Assistant")
        self._root.geometry("400x260")
        self._root.resizable(False, False)
        self._root.protocol("WM_DELETE_WINDOW", self._root.withdraw)

        tk.Label(self._root, text="Voice Assistant", font=("Segoe UI", 14, "bold")).pack(pady=(15, 4))

        self._status_var = tk.StringVar(value="Idle")
        tk.Label(self._root, textvariable=self._status_var, font=("Segoe UI", 10), fg="#555").pack()

        tk.Label(self._root, text="Last transcription (click to select):", font=("Segoe UI", 9), fg="#888").pack(pady=(12, 2))
        self._transcript_var = tk.StringVar(value="—")
        self._transcript_entry = tk.Entry(self._root, textvariable=self._transcript_var,
                                          font=("Segoe UI", 10), relief=tk.FLAT,
                                          bg="#f0f0f0", readonlybackground="#f0f0f0",
                                          state="readonly", width=46)
        self._transcript_entry.pack(padx=10)

        btn = tk.Frame(self._root)
        btn.pack(pady=12)
        tk.Button(btn, text="Play Response", command=self._on_tts_play, width=14).pack(side=tk.LEFT, padx=5)
        self._mute_var = tk.BooleanVar()
        tk.Checkbutton(btn, text="Mute", variable=self._mute_var,
                       command=lambda: self._on_mute_toggle(self._mute_var.get())).pack(side=tk.LEFT, padx=5)

        tk.Button(self._root, text="Settings", command=self._on_open_settings, width=12).pack(pady=4)

    def set_status(self, status: str) -> None:
        if self._root and self._status_var:
            self._root.after(0, lambda s=status: self._status_var.set(s))

    def set_transcript(self, text: str) -> None:
        if self._root and self._transcript_var:
            short = text[:80] + "..." if len(text) > 80 else text
            self._root.after(0, lambda t=short: self._transcript_var.set(t))

    def mainloop(self) -> None:
        if self._root:
            self._root.mainloop()

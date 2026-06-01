import tkinter as tk
import threading
from typing import Callable

class TranscriptionPreview:
    def __init__(self, timeout_seconds: int, on_confirm: Callable[[str], None], on_cancel: Callable[[], None]):
        self._timeout = timeout_seconds
        self._on_confirm = on_confirm
        self._on_cancel = on_cancel

    def show(self, text: str) -> None:
        threading.Thread(target=self._run, args=(text,), daemon=True).start()

    def _run(self, text: str) -> None:
        root = tk.Tk()
        root.title("")
        root.attributes("-topmost", True)
        root.resizable(False, False)
        w, h = 500, 120
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry(f"{w}x{h}+{(sw - w) // 2}+{sh - h - 80}")

        tk.Label(root, text=f"Transcribed (sending in {self._timeout}s):", font=("Segoe UI", 9)).pack(pady=(10, 2))
        tk.Label(root, text=text, font=("Segoe UI", 11, "bold"), wraplength=460).pack()

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Send", command=lambda: self._confirm(root, text), bg="#0078d4", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=lambda: self._cancel(root)).pack(side=tk.LEFT, padx=5)

        root.after(self._timeout * 1000, lambda: self._confirm(root, text))
        root.mainloop()

    def _confirm(self, root: tk.Tk, text: str) -> None:
        try:
            root.destroy()
        except tk.TclError:
            pass
        self._on_confirm(text)

    def _cancel(self, root: tk.Tk) -> None:
        try:
            root.destroy()
        except tk.TclError:
            pass
        self._on_cancel()

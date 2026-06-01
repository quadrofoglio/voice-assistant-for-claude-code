# Voice Assistant — Handoff Document

## What Was Built

A Windows desktop companion app that gives Claude Code CLI a voice interface:
- **Speech-to-text**: press `Ctrl+Shift+R` to start/stop recording, faster-whisper transcribes locally (offline, free)
- **Text delivery**: auto-types into terminal or copies to clipboard (always copies to clipboard as backup)
- **Text-to-speech**: press `Alt+R` to hear Claude's last response; edge-tts (online, neural) with Piper TTS fallback (offline, neural)
- **Claude Code integration**: Stop hook auto-installed to `~/.claude/settings.json` — forwards every response to the app via local TCP socket
- **UI**: system tray icon + main window + settings panel (tkinter)

## App Location

**Installed at:** `C:\Users\limfy\AppData\Local\VoiceAssistant\VoiceAssistant.exe`

**Source code:** `C:\Users\limfy\OneDrive\Documents\speech-to-text-to-LLM\`

**GitHub:** https://github.com/quadrofoglio/voice-assistant-for-claude-code

## Architecture

```
src/
  main.py           — App class, wires all components
  settings.py       — JSON config load/save (~/.voice_assistant/settings.json)
  stt.py            — Microphone recording + faster-whisper transcription
  tts.py            — TTS orchestrator (edge-tts primary, Piper fallback)
  tts_edge.py       — edge-tts async→sync wrapper
  tts_piper.py      — Piper TTS via subprocess (piper.exe binary)
  text_cleaner.py   — Strips code blocks/markdown from responses before TTS
  input_delivery.py — auto-type (pynput) or clipboard (pyperclip)
  hotkey_manager.py — Global toggle hotkeys via keyboard library
  socket_server.py  — Local TCP server receives hook data from Claude
  hook_installer.py — Writes Stop hook to ~/.claude/settings.json on first run
  preview.py        — Transcription preview overlay (2s auto-confirm)
  tray.py           — pystray system tray icon
  window.py         — Main tkinter window
  settings_panel.py — Settings UI (3-tab notebook)
  piper_manager.py  — Download/manage Piper voice models
  paths.py          — sys._MEIPASS helpers for PyInstaller bundle paths

hook/
  stop_hook.py      — Claude Code Stop hook script (runs on every response)

config/
  default_settings.json — Default settings (stt_hotkey, voices, socket_port, etc.)

voices/             — Piper voice files (.onnx + .onnx.json) — NOT in git (too large)
piper_bin/          — piper.exe binary — NOT in git (too large)
```

## Key Design Decisions

| Decision | Reason |
|---|---|
| Toggle mode (press once to start, press again to stop) | `Alt+Space` hold-to-talk failed — Windows intercepts key releases when system menus are triggered |
| Default hotkey `ctrl+shift+r` | Safe on Windows, doesn't conflict with system shortcuts |
| Subprocess for Piper TTS | `piper-tts` pip package has no wheel for Python 3.12 on Windows |
| `sys._MEIPASS` via `src/paths.py` | PyInstaller `--onedir` puts bundled data in `_internal/`, not next to exe |
| Build to `C:\Temp`, deploy to `AppData\Local` | Source is in OneDrive — file locking during builds when building in-place |
| Always copy to clipboard in both modes | Auto-type can fail if terminal loses focus; clipboard is a reliable fallback |

## How to Rebuild

After making code changes:

```powershell
cd "C:\Users\limfy\OneDrive\Documents\speech-to-text-to-LLM"

# 1. Kill the running app first (it locks DLLs)
Stop-Process -Name "VoiceAssistant" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# 2. Build to Temp (avoids OneDrive locking)
.\venv\Scripts\activate
pyinstaller --noconfirm --name VoiceAssistant --onedir --windowed `
  --icon assets/icon.ico `
  --add-data "config;config" --add-data "assets;assets" --add-data "hook;hook" `
  --add-binary "C:\Users\limfy\anaconda3\Library\bin\ffi-8.dll;." `
  --add-binary "C:\Users\limfy\anaconda3\Library\bin\ffi-7.dll;." `
  --add-binary "C:\Users\limfy\anaconda3\Library\bin\ffi.dll;." `
  --distpath "C:\Temp\VoiceAssistantDist" src/main.py

# 3. Copy missing Anaconda DLLs
$build = "C:\Temp\VoiceAssistantDist\VoiceAssistant"
foreach ($dll in @("tcl86t.dll","tk86t.dll","sqlite3.dll","libssl-3-x64.dll","liblzma.dll","libbz2.dll")) {
    Copy-Item "C:\Users\limfy\anaconda3\envs\py311-smu\Library\bin\$dll" $build
}
Copy-Item "C:\Users\limfy\anaconda3\envs\pylearn\Library\bin\libexpat.dll" $build

# 4. Copy runtime data (voices and piper binary)
Copy-Item -Recurse voices "$build\voices"
Copy-Item -Recurse piper_bin "$build\piper_bin"

# 5. Deploy to permanent location
Remove-Item -Recurse -Force "C:\Users\limfy\AppData\Local\VoiceAssistant"
Copy-Item -Recurse $build "C:\Users\limfy\AppData\Local\VoiceAssistant"

Write-Host "Done: C:\Users\limfy\AppData\Local\VoiceAssistant\VoiceAssistant.exe"
```

## How to Run from Source (no exe)

```powershell
cd "C:\Users\limfy\OneDrive\Documents\speech-to-text-to-LLM"
.\venv\Scripts\activate
python src/main.py
```

## Running Tests

```powershell
.\venv\Scripts\activate
pytest tests/ -v --ignore=tests/test_stt_manual.py --ignore=tests/test_tts_edge_manual.py --ignore=tests/test_tts_piper_manual.py
```

Expected: 24 tests pass (manual tests skipped — require microphone/speakers).

## Known Issues & Next Steps

| Issue | Status | Suggested Fix |
|---|---|---|
| First transcription slow (10–15s) | Existing | Pre-warm Whisper model on startup in background thread |
| Wake word not implemented | Stub in settings UI | Wire up `openwakeword` library in `stt.py` |
| No visual feedback during transcription | Existing | Add a progress spinner or animated indicator |
| Transcription preview auto-send countdown not visible | Minor | Show a countdown number in the overlay |
| Build requires manual DLL copying | Existing | Add all DLLs to `build.ps1` with `--add-binary` flags |
| TTS playback uses OS default player (temp .mp3/.wav) | Existing | Use `sounddevice` or `pygame` for direct playback |
| Settings panel opens in a thread (occasional flicker) | Minor | Move settings panel to run on main thread via `root.after()` |

## Python Environment

- **Python:** 3.12.3 (conda-forge, via Anaconda)
- **Venv:** `C:\Users\limfy\OneDrive\Documents\speech-to-text-to-LLM\venv\`
- **Key packages:** faster-whisper, edge-tts, pystray, pynput, keyboard, sounddevice, pyperclip, pillow

## Credentials / API Keys

None required. All components are free and run locally or use free online services (edge-tts uses Microsoft's public neural TTS endpoint — no key needed).

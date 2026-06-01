# Voice Assistant build script
.\venv\Scripts\activate

pyinstaller `
  --name VoiceAssistant `
  --onefile `
  --windowed `
  --icon assets/icon.ico `
  --add-data "config;config" `
  --add-data "assets;assets" `
  --add-data "hook;hook" `
  src/main.py

Write-Host "Build complete: dist/VoiceAssistant.exe"

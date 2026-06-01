# Voice Assistant build script
.\venv\Scripts\activate

pyinstaller `
  --name VoiceAssistant `
  --onedir `
  --windowed `
  --icon assets/icon.ico `
  --add-data "config;config" `
  --add-data "assets;assets" `
  --add-data "hook;hook" `
  --add-binary "C:\Users\limfy\anaconda3\Library\bin\ffi-8.dll;." `
  --add-binary "C:\Users\limfy\anaconda3\Library\bin\ffi-7.dll;." `
  --add-binary "C:\Users\limfy\anaconda3\Library\bin\ffi.dll;." `
  src/main.py

Write-Host "Build complete: dist/VoiceAssistant/VoiceAssistant.exe"

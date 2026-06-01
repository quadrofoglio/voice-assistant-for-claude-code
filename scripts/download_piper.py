"""Run once to download piper.exe: python scripts/download_piper.py"""
import urllib.request, zipfile, pathlib, os

PIPER_VERSION = "2023.11.14-2"
URL = f"https://github.com/rhasspy/piper/releases/download/{PIPER_VERSION}/piper_windows_amd64.zip"
DEST_DIR = pathlib.Path("piper_bin")

def download():
    DEST_DIR.mkdir(exist_ok=True)
    zip_path = DEST_DIR / "piper.zip"
    print(f"Downloading piper {PIPER_VERSION}...")
    urllib.request.urlretrieve(URL, zip_path)
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall(DEST_DIR)
    zip_path.unlink()
    exe = next(DEST_DIR.rglob("piper.exe"), None)
    if exe:
        print(f"piper.exe at: {exe}")
    else:
        print("ERROR: piper.exe not found in zip")

if __name__ == "__main__":
    download()

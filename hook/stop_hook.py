#!/usr/bin/env python3
"""Claude Code Stop hook. Reads response JSON from stdin, sends prose text to companion app."""
import sys
import json
import socket

SOCKET_PORT = 47291

def extract_last_assistant_text(transcript: list) -> str:
    for msg in reversed(transcript):
        if msg.get("role") != "assistant":
            continue
        content = msg.get("content", "")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = [b["text"] for b in content if b.get("type") == "text"]
            return "\n".join(parts)
    return ""

def send_to_app(text: str, port: int) -> None:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2.0)
            s.connect(("127.0.0.1", port))
            s.sendall((json.dumps({"text": text}) + "\n").encode())
    except (ConnectionRefusedError, socket.timeout):
        pass  # Companion app not running — silently skip

def main():
    raw = sys.stdin.read()
    if not raw.strip():
        return
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return
    text = extract_last_assistant_text(data.get("transcript", []))
    if text:
        send_to_app(text, SOCKET_PORT)

if __name__ == "__main__":
    main()

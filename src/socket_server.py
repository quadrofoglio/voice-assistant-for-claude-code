import socket
import threading
import json
from typing import Callable

class SocketServer:
    def __init__(self, port: int, on_message: Callable[[dict], None]):
        self._port = port
        self._on_message = on_message
        self._server_socket = None
        self._running = False

    def start(self) -> None:
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind(("127.0.0.1", self._port))
        self._server_socket.listen(5)
        self._server_socket.settimeout(1.0)
        self._running = True
        while self._running:
            try:
                conn, _ = self._server_socket.accept()
                threading.Thread(target=self._handle, args=(conn,), daemon=True).start()
            except socket.timeout:
                continue
        self._server_socket.close()

    def stop(self) -> None:
        self._running = False

    def _handle(self, conn: socket.socket) -> None:
        with conn:
            data = b""
            while chunk := conn.recv(4096):
                data += chunk
                if b"\n" in data:
                    break
            if data:
                try:
                    msg = json.loads(data.decode().strip())
                    self._on_message(msg)
                except json.JSONDecodeError:
                    pass

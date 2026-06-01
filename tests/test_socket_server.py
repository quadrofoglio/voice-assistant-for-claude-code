import threading, socket, time, json
from src.socket_server import SocketServer

def test_server_receives_message():
    received = []
    server = SocketServer(port=47292, on_message=lambda msg: received.append(msg))
    t = threading.Thread(target=server.start, daemon=True)
    t.start()
    time.sleep(0.1)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("127.0.0.1", 47292))
        s.sendall(json.dumps({"text": "hello"}).encode() + b"\n")

    time.sleep(0.15)
    server.stop()
    assert received == [{"text": "hello"}]

def test_server_handles_multiple_connections():
    received = []
    server = SocketServer(port=47293, on_message=lambda msg: received.append(msg))
    t = threading.Thread(target=server.start, daemon=True)
    t.start()
    time.sleep(0.1)

    for i in range(3):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("127.0.0.1", 47293))
            s.sendall(json.dumps({"text": f"msg{i}"}).encode() + b"\n")
        time.sleep(0.05)

    time.sleep(0.15)
    server.stop()
    assert len(received) == 3

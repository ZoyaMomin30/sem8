# Experiment 1: Inter-Process Communication (IPC) using TCP Sockets

import socket
import threading

def server():
    s = socket.socket()
    s.bind(('localhost', 9999))
    s.listen(1)
    print("[Server] Waiting for connection...")
    conn, addr = s.accept()
    print(f"[Server] Connected by {addr}")
    msg = conn.recv(1024).decode()
    print(f"[Server] Received: {msg}")
    conn.send("Hello from Server!".encode())
    conn.close()

def client():
    s = socket.socket()
    s.connect(('localhost', 9999))
    s.send("Hello from Client!".encode())
    reply = s.recv(1024).decode()
    print(f"[Client] Server replied: {reply}")
    s.close()

# Run server in background thread, then client
t = threading.Thread(target=server)
t.start()

import time; time.sleep(0.5)  # let server start
client()
t.join()

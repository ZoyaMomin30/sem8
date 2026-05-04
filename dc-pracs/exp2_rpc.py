# Experiment 2: Client-Server using RPC (simulated in Python)
# Client calls a remote function by name + args over a socket.
# Server receives, executes, and returns the result.

import socket
import threading
import json

# ── Server ────────────────────────────────────────────────────────────────────

def add(a, b):      return a + b
def multiply(a, b): return a * b
def greet(name):    return f"Hello, {name}!"

FUNCTIONS = {"add": add, "multiply": multiply, "greet": greet}

def server():
    s = socket.socket()
    s.bind(('localhost', 9998))
    s.listen(5)
    print("[Server] RPC Server started...")
    while True:
        conn, _ = s.accept()
        data = json.loads(conn.recv(1024).decode())
        func_name = data["func"]
        args      = data["args"]
        print(f"[Server] Call: {func_name}({args})")
        result = FUNCTIONS[func_name](*args)
        conn.send(json.dumps({"result": result}).encode())
        conn.close()

# ── Client (stub) ─────────────────────────────────────────────────────────────

def rpc_call(func_name, *args):
    s = socket.socket()
    s.connect(('localhost', 9998))
    s.send(json.dumps({"func": func_name, "args": args}).encode())
    result = json.loads(s.recv(1024).decode())["result"]
    s.close()
    return result

# ── Run ───────────────────────────────────────────────────────────────────────

t = threading.Thread(target=server, daemon=True)
t.start()

import time; time.sleep(0.3)

print("[Client] add(3, 4)      =", rpc_call("add", 3, 4))
print("[Client] multiply(6, 7) =", rpc_call("multiply", 6, 7))
print("[Client] greet('Alice') =", rpc_call("greet", "Alice"))

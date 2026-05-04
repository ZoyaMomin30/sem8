# ricart_agrawala.py
import threading
import time
import random

N = 3  # number of processes

class Process:
    def __init__(self, pid):
        self.pid = pid
        self.clock = 0
        self.requesting = False
        self.reply_count = 0

    def request_cs(self):
        self.clock += 1
        self.requesting = True
        self.reply_count = 0

        print(f"Process {self.pid} requesting CS at time {self.clock}")

        # Send request to all other processes
        for p in processes:
            if p.pid != self.pid:
                p.receive_request(self.pid, self.clock)

        # Wait until all replies received
        while self.reply_count < N - 1:
            time.sleep(0.1)

        self.enter_cs()

    def receive_request(self, from_pid, timestamp):
        self.clock = max(self.clock, timestamp) + 1
        print(f"Process {self.pid} received request from {from_pid}")

        # Send reply immediately (simplified logic)
        processes[from_pid - 1].receive_reply()

    def receive_reply(self):
        self.reply_count += 1

    def enter_cs(self):
        print(f"Process {self.pid} ENTERING Critical Section\n")
        time.sleep(2)
        print(f"Process {self.pid} EXITING Critical Section\n")
        self.requesting = False


# Create processes
processes = [Process(i+1) for i in range(N)]

# Simulate processes requesting CS
threads = []
for p in processes:
    t = threading.Thread(target=p.request_cs)
    threads.append(t)
    t.start()
    time.sleep(random.uniform(0.5, 1.5))

for t in threads:
    t.join()

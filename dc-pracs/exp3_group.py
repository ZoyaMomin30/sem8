# Experiment 3: Group Communication (simulated multicast)
# One sender multicasts a message to a group of receiver threads.
# Demonstrates FIFO ordering: each receiver gets messages in send order.

import threading
import queue
import time

# Lock to prevent jumbled print output from concurrent threads
print_lock = threading.Lock()

# Each group member gets their own message queue
group = {f"P{i}": queue.Queue() for i in range(1, 5)}

def multicast(sender, message):
    """Send message to all group members."""
    with print_lock:
        print(f"\n[{sender}] Multicasting: '{message}'")
    for name, q in group.items():
        q.put((sender, message))

def member(name):
    """Group member — receives and prints messages."""
    q = group[name]
    while True:
        sender, msg = q.get()
        with print_lock:
            print(f"  [{name}] Received from {sender}: '{msg}'")
        q.task_done()
        if msg == "STOP":
            break

# Start all member threads
threads = [threading.Thread(target=member, args=(name,)) for name in group]
for t in threads: t.start()

time.sleep(0.2)

# Sender multicasts messages — receivers get them in order (FIFO)
multicast("Coordinator", "Meeting at 10am")
multicast("Coordinator", "Bring laptops")
multicast("Coordinator", "STOP")

for t in threads: t.join()
print("\nAll members received all messages.")
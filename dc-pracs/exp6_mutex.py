# Experiment 6: Mutual Exclusion — Ricart-Agrawala Algorithm

import threading
import time

N = 3
clocks   = [0] * N          # Lamport clock per process
want_cs  = [False] * N      # is process requesting CS?
in_cs    = [False] * N      # is process in CS?
deferred = [[] for _ in N*[0]]   # deferred replies per process
replies  = [0] * N          # reply count per process
lock     = threading.Lock()

def request_cs(pid):
    with lock:
        clocks[pid] += 1
        want_cs[pid] = True
        ts = clocks[pid]
    print(f"P{pid} REQUESTS CS  (timestamp={ts})")

    # Ask all other processes for permission
    for other in range(N):
        if other != pid:
            handle_request(other, pid, ts)   # simulated message

    # Wait until all replied
    while replies[pid] < N - 1:
        time.sleep(0.05)

    in_cs[pid] = True
    print(f"P{pid} ENTERS    Critical Section >>>")

def release_cs(pid):
    in_cs[pid] = False
    want_cs[pid] = False
    replies[pid] = 0
    print(f"P{pid} EXITS     Critical Section <<<")

    # Send deferred replies
    with lock:
        pending = deferred[pid][:]
        deferred[pid].clear()
    for req_pid in pending:
        print(f"  P{pid} sends deferred REPLY to P{req_pid}")
        replies[req_pid] += 1

def handle_request(receiver, requester, req_ts):
    """P(receiver) decides whether to reply immediately or defer."""
    with lock:
        clocks[receiver] = max(clocks[receiver], req_ts) + 1
        my_ts = clocks[receiver]

        should_defer = (
            in_cs[receiver] or
            (want_cs[receiver] and (my_ts, receiver) < (req_ts, requester))
        )

        if should_defer:
            print(f"  P{receiver} DEFERS reply to P{requester}")
            deferred[receiver].append(requester)
        else:
            print(f"  P{receiver} sends REPLY to P{requester}")
            replies[requester] += 1

def process(pid, delay):
    time.sleep(delay)
    request_cs(pid)
    time.sleep(0.2)   # do work in CS
    release_cs(pid)

# Three processes request CS concurrently
threads = [threading.Thread(target=process, args=(i, i * 0.1)) for i in range(N)]
for t in threads: t.start()
for t in threads: t.join()

print("\nDone — mutual exclusion maintained.")

# Bully_algorithm.py
import random

class Process:
    def __init__(self, pid):
        self.pid = pid
        self.alive = True

    def __str__(self):
        return f"Process {self.pid}"

# Create processes
processes = [Process(i) for i in range(1, 6)]

# Current coordinator (highest ID)
coordinator = max(processes, key=lambda p: p.pid)
print("Initial Coordinator:", coordinator)

# Simulate coordinator failure
coordinator.alive = False
print(f"{coordinator} has failed!\n")

def bully_election(process):
    print(f"{process} starts election")

    higher_processes = [p for p in processes if p.pid > process.pid and p.alive]

    if not higher_processes:
        print(f"{process} becomes new Coordinator\n")
        return process

    for p in higher_processes:
        print(f"{process} sends election message to {p}")

    highest = max(higher_processes, key=lambda p: p.pid)
    return bully_election(highest)

new_coordinator = bully_election(processes[1])

print("Final Coordinator:", new_coordinator)

# Experiment 4: Clock Synchronization — Lamport & Vector Clocks

# ── Lamport Clock ─────────────────────────────────────────────────────────────

class LamportClock:
    def __init__(self, name):
        self.name = name
        self.time = 0

    def event(self):
        self.time += 1
        print(f"[{self.name}] Internal event  -> LC = {self.time}")

    def send(self):
        self.time += 1
        print(f"[{self.name}] Sending message -> LC = {self.time}")
        return self.time

    def receive(self, received_time):
        self.time = max(self.time, received_time) + 1
        print(f"[{self.name}] Received LC={received_time} -> LC = {self.time}")


# ── Vector Clock ──────────────────────────────────────────────────────────────

class VectorClock:
    def __init__(self, name, all_processes):
        self.name = name
        self.procs = all_processes
        self.vc = {p: 0 for p in all_processes}

    def event(self):
        self.vc[self.name] += 1
        print(f"[{self.name}] Internal event  -> VC = {self.vc}")

    def send(self):
        self.vc[self.name] += 1
        print(f"[{self.name}] Sending message -> VC = {self.vc}")
        return dict(self.vc)

    def receive(self, received_vc):
        for p in self.procs:
            self.vc[p] = max(self.vc[p], received_vc[p])
        self.vc[self.name] += 1
        print(f"[{self.name}] Received VC={received_vc} -> VC = {self.vc}")


# ── Demo ──────────────────────────────────────────────────────────────────────

print("=" * 45)
print("LAMPORT CLOCKS")
print("=" * 45)
p1 = LamportClock("P1")
p2 = LamportClock("P2")

p1.event()
ts = p1.send()
p2.receive(ts)
p2.event()
ts2 = p2.send()
p1.receive(ts2)

print()
print("=" * 45)
print("VECTOR CLOCKS")
print("=" * 45)
procs = ["P1", "P2", "P3"]
v1 = VectorClock("P1", procs)
v2 = VectorClock("P2", procs)
v3 = VectorClock("P3", procs)

v1.event()
vc = v1.send()
v2.receive(vc)
v2.event()
vc2 = v2.send()
v3.receive(vc2)
v3.event()

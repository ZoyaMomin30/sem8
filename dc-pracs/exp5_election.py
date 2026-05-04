# Experiment 5: Election Algorithms — Bully & Ring

# ── Bully Algorithm ───────────────────────────────────────────────────────────

def bully_election(processes, failed):
    print("=" * 40)
    print(f"BULLY ALGORITHM  |  Failed: P{failed}")
    print("=" * 40)
    active = [p for p in processes if p != failed]

    initiator = min(active)  # lowest ID notices failure first
    print(f"P{initiator} detects failure, starts election")

    coordinator = initiator
    for p in active:
        if p > coordinator:
            print(f"P{p} responds OK — takes over election")
            coordinator = p

    print(f"Result: P{coordinator} is the new Coordinator\n")


# ── Ring Algorithm ────────────────────────────────────────────────────────────

def ring_election(processes, failed):
    print("=" * 40)
    print(f"RING ALGORITHM   |  Failed: P{failed}")
    print("=" * 40)
    active = [p for p in processes if p != failed]
    n = len(active)

    initiator = active[0]
    print(f"P{initiator} starts election, sending token around ring")

    token = initiator
    current = active[1 % n]

    for i in range(1, n):
        current = active[i % n]
        if current > token:
            print(f"  P{current} sees token={token}, replaces with {current}")
            token = current
        else:
            print(f"  P{current} forwards token={token}")

    print(f"Token returns to P{initiator}: highest ID = {token}")
    print(f"Result: P{token} is the new Coordinator\n")


# ── Run both ──────────────────────────────────────────────────────────────────

processes = [1, 2, 3, 4, 5]
failed    = 5   # coordinator failed

bully_election(processes, failed)
ring_election(processes, failed)

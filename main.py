import threading
import random
import time
import sys

COLORS = [
    "\033[91m",
    "\033[92m",
    "\033[93m",
    "\033[94m",
    "\033[95m",
    "\033[96m",
]
RESET = "\033[0m"

price_per_unit = 5

def progress_bar(done, total, width=20, color=""):
    filled = int(width * done / total)
    bar = "#" * filled + "-" * (width - filled)
    return f"{color}[{bar}] {done}/{total}{RESET}"

class Warehouse:
    def __init__(self, name, meds):
        self.name = name
        self.meds = meds
        self.lock = threading.Lock()

    def steal(self, amount):
        outcome = random.choice(["full", "partial", "fail", "caught"])

        if outcome in ("fail", "caught"):
            return 0, "невдача" if outcome == "fail" else "спіймано охороною"

        with self.lock:
            if self.meds <= 0:
                return 0, "порожньо"

            if outcome == "full":
                stolen = min(amount, self.meds)
            else:
                stolen = min(random.randint(1, amount), self.meds)

            self.meds -= stolen
            return stolen, ("успіх" if outcome == "full" else "частково")

class Runner(threading.Thread):
    def __init__(self, name, warehouse, runner_id, color):
        super().__init__()
        self.name = name
        self.warehouse = warehouse
        self.runner_id = runner_id
        self.color = color
        self.loot = 0
        self.attempts_done = 0
        self.total_attempts = 10
        self.last_status = ""

    def run(self):
        for _ in range(self.total_attempts):
            amount = random.randint(10, 30)
            stolen, status = self.warehouse.steal(amount)
            self.last_status = status

            if stolen > 0:
                self.loot += stolen * price_per_unit

            self.attempts_done += 1
            time.sleep(random.uniform(0.1, 0.5))

def draw_progress(runners):
    print("\nПРОГРЕС БІГУНІВ:")
    for r in runners:
        bar = progress_bar(r.attempts_done, r.total_attempts, color=r.color)
        print(f"{r.color}{r.name}{RESET}: {bar}  ({r.last_status})")
    print("\n")

def run_simulation(sim_number=1):
    print(f"\n\033[95m==================== СИМУЛЯЦІЯ #{sim_number} ====================\033[0m\n")

    warehouses = [Warehouse(f"Склад-{i}", random.randint(100, 300)) for i in range(1, 4)]

    runners = []
    for i in range(5):
        runner = Runner(
            f"Runner-{i+1}",
            random.choice(warehouses),
            i+1,
            COLORS[i % len(COLORS)]
        )
        runners.append(runner)

    for r in runners:
        r.start()

    while any(r.is_alive() for r in runners):
        draw_progress(runners)
        time.sleep(0.3)

    for r in runners:
        r.join()

    draw_progress(runners)

    print("\n\033[93m=== РЕЗУЛЬТАТИ СИМУЛЯЦІЇ ===\033[0m\n")

    total_loot = sum(r.loot for r in runners)

    for w in warehouses:
        print(f"\033[94m{w.name}\033[0m: залишилось {w.meds} одиниць")

    for r in runners:
        print(f"{r.color}{r.name}{RESET} заробив: {r.loot} валютних одиниць")

    print(f"\n\033[92mЗАГАЛОМ зароблено: {total_loot} валютних одиниць\033[0m\n")

    return total_loot

if __name__ == "__main__":
    for i in range(1, 4):
        run_simulation(i)

from typing import List, Dict
from dataclasses import dataclass
from colorama import Fore, Style

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Optimize a 3D print queue according to job priorities and printer constraints.
    Uses a greedy algorithm to batch jobs without exceeding volume or item limits.

    Args:
        print_jobs: List of print job dicts
        constraints: Dict of printer constraints

    Returns:
        Dict with keys:
            "print_order": List of job IDs in printing order
            "total_time": Total printing time in minutes
    """

    jobs = [PrintJob(**job) for job in print_jobs]
    cons = PrinterConstraints(**constraints)
    
    jobs.sort(key=lambda job: job.priority)
    
    batches = []
    current_batch = []
    current_volume = 0.0
    
    for job in jobs:
        if not current_batch:
            current_batch = [job]
            current_volume = job.volume
        else:
            if (len(current_batch) + 1 <= cons.max_items and
                current_volume + job.volume <= cons.max_volume):
                current_batch.append(job)
                current_volume += job.volume
            else:
                batches.append(current_batch)
                current_batch = [job]
                current_volume = job.volume
    
    if current_batch:
        batches.append(current_batch)
    
    total_time = sum(max(j.print_time for j in batch) for batch in batches)
    print_order = [j.id for batch in batches for j in batch]
    
    return {"print_order": print_order, "total_time": total_time}

# Testing
def test_printing_optimization():
    
    tests = [
        ("Test 1 (same priority)", [
            {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
            {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
            {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
        ]),
        ("Test 2 (mixed priorities)", [
            {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
            {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
            {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}
        ]),
        ("Test 3 (exceeding constraints)", [
            {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
            {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
            {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
        ])
    ]

    constraints = {"max_volume": 300, "max_items": 2}
    
    for name, jobs in tests:
        result = optimize_printing(jobs, constraints)
        print(Fore.YELLOW + f"{name}:" + Style.RESET_ALL)
        print(f"  Print order: {result['print_order']}")
        print(Fore.GREEN + f"  Total time: {result['total_time']} minutes\n" + Style.RESET_ALL)

if __name__ == "__main__":
    test_printing_optimization()

"""
Runs timing experiments for Part 1 (quicksort comparison) and
Part 2 (hash table operations) and prints results in a readable table.
"""

import random
import time
import sys

from quicksort import sort_randomized, sort_deterministic
from hash_table import HashTable

# ---------------------------------------------------------------
# Part 1 helpers
# ---------------------------------------------------------------

SIZES = [500, 1000, 2000, 5000, 10000]
SMALL_SIZES = [500, 1000, 2000]   # deterministic on sorted can blow stack


def timed(func, arr, runs=3):
    """Return average time in ms over `runs` repetitions."""
    total = 0.0
    for _ in range(runs):
        a = arr[:]
        t0 = time.perf_counter()
        func(a)
        total += time.perf_counter() - t0
    return (total / runs) * 1000   # milliseconds


def make_random(n):
    return [random.randint(0, 10 * n) for _ in range(n)]


def make_sorted(n):
    return list(range(n))


def make_reverse(n):
    return list(range(n, 0, -1))


def make_repeated(n):
    return [random.choice([1, 2, 3, 4, 5]) for _ in range(n)]


DISTRIBUTIONS = {
    "Random":    (make_random,   SIZES),
    "Sorted":    (make_sorted,   SMALL_SIZES),
    "Reverse":   (make_reverse,  SMALL_SIZES),
    "Repeated":  (make_repeated, SIZES),
}


def run_quicksort_experiments():
    print("\n=== Part 1: Quicksort Timing (ms) ===\n")
    header = f"{'Distribution':<12} {'n':>6}  {'Randomized':>12}  {'Deterministic':>14}"
    print(header)
    print("-" * len(header))

    results = {}
    for dist_name, (maker, sizes) in DISTRIBUTIONS.items():
        for n in sizes:
            arr = maker(n)
            t_rand = timed(sort_randomized, arr)
            try:
                t_det = timed(sort_deterministic, arr)
                det_str = f"{t_det:>14.3f}"
            except RecursionError:
                det_str = f"{'RecursionError':>14}"
                t_det = None
            print(f"{dist_name:<12} {n:>6}  {t_rand:>12.3f}  {det_str}")
            results[(dist_name, n)] = (t_rand, t_det)
    return results


# ---------------------------------------------------------------
# Part 2 helpers
# ---------------------------------------------------------------

def run_hash_experiments():
    print("\n=== Part 2: Hash Table Operation Times (µs) ===\n")
    ns = [1000, 5000, 10000, 50000]

    header = f"{'n':>8}  {'load_factor':>12}  {'insert (µs)':>12}  {'search_hit (µs)':>16}  {'search_miss (µs)':>17}  {'delete (µs)':>12}"
    print(header)
    print("-" * len(header))

    for n in ns:
        ht = HashTable()
        keys = list(range(n))
        random.shuffle(keys)

        # insert all
        t0 = time.perf_counter()
        for k in keys:
            ht.insert(k, k * 2)
        t_insert = (time.perf_counter() - t0) / n * 1e6

        lf = ht.load_factor

        # successful search (keys that exist)
        sample_hit = random.choices(keys, k=min(1000, n))
        t0 = time.perf_counter()
        for k in sample_hit:
            ht.search(k)
        t_search_hit = (time.perf_counter() - t0) / len(sample_hit) * 1e6

        # unsuccessful search (keys that don't exist)
        miss_keys = [n + i for i in range(1000)]
        t0 = time.perf_counter()
        for k in miss_keys:
            ht.search(k)
        t_search_miss = (time.perf_counter() - t0) / len(miss_keys) * 1e6

        # delete half the keys
        del_keys = random.choices(keys, k=n // 2)
        t0 = time.perf_counter()
        for k in del_keys:
            ht.delete(k)
        t_delete = (time.perf_counter() - t0) / len(del_keys) * 1e6

        print(f"{n:>8}  {lf:>12.3f}  {t_insert:>12.4f}  {t_search_hit:>16.4f}  {t_search_miss:>17.4f}  {t_delete:>12.4f}")


# ---------------------------------------------------------------
# Main
# ---------------------------------------------------------------

if __name__ == "__main__":
    random.seed(42)
    run_quicksort_experiments()
    run_hash_experiments()

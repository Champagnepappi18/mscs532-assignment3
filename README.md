# MSCS 532 – Assignment 3: Algorithm Efficiency and Scalability

**University of the Cumberlands**  
**Course:** MSCS 532 – Algorithms and Data Structures (MSCS-532-M20)  
**Student:** Mayur Patel  
**Date:** June 7, 2026

---

## Overview

This repository contains the implementation, analysis, and empirical comparison for two fundamental algorithms:

- **Part 1 — Randomized Quicksort:** Implementation of randomized and deterministic quicksort, theoretical proof that average-case time is O(n log n), and empirical comparison across four input distributions.
- **Part 2 — Hash Table with Chaining:** Implementation of a hash table using linked-list chaining with a universal hash function and dynamic resizing, along with theoretical and empirical analysis of all operations.

---

## Repository Structure

```
.
├── quicksort.py                        # Part 1 — Randomized and Deterministic Quicksort
├── hash_table.py                       # Part 2 — Hash Table with Chaining
├── experiments.py                      # Timing experiments for both parts
├── Assignment3_MayurPatel_Report.docx  # Full report (formatted, with title page)
├── report.md                           # Same report in Markdown format
└── README.md                           # This file
```

---

## How to Run

**Requirements:** Python 3.8 or higher. No external libraries needed.

### Run all experiments

```bash
python experiments.py
```

This prints two timing tables:
1. Randomized vs. Deterministic Quicksort across four input types and multiple sizes
2. Hash table insert / search (hit & miss) / delete times for n = 1,000 to 50,000

### Use Quicksort directly

```python
from quicksort import sort_randomized, sort_deterministic

arr = [5, 3, 8, 1, 9, 2]

sorted_arr = sort_randomized(arr)
print(sorted_arr)   # [1, 2, 3, 5, 8, 9]

sorted_arr2 = sort_deterministic(arr)
print(sorted_arr2)  # [1, 2, 3, 5, 8, 9]
```

### Use the Hash Table directly

```python
from hash_table import HashTable

ht = HashTable()

# Insert
ht.insert("name", "Mayur")
ht.insert("course", "MSCS 532")
ht.insert("year", 2026)

# Search
print(ht.search("name"))    # Mayur
print(ht.search("missing")) # None

# Delete
ht.delete("year")
print(ht.search("year"))    # None

print(len(ht))              # 2
print(ht.load_factor)       # current load factor (float)
```

---

## Key Results

### Part 1 — Quicksort

| Input Type | n | Randomized (ms) | Deterministic (ms) |
|:-----------|--:|----------------:|-------------------:|
| Random | 10,000 | 9.278 | 8.376 |
| Sorted | 2,000 | 1.536 | **45.122** |
| Reverse | 2,000 | 1.509 | **78.003** |
| Repeated | 10,000 | 560.151 | 563.194 |

- On **sorted input**, deterministic quicksort grows at roughly **4× per 2× increase in n** — the signature of O(n²) growth. Randomized quicksort stays at ~2.2× per 2× increase, consistent with O(n log n).
- On **random input**, both perform similarly. The randomized version adds slight overhead from random number generation.
- On **repeated elements**, both degrade equally because Lomuto partitioning does not split equal-valued elements well.

### Part 2 — Hash Table

| n | Load Factor | Search Hit (µs) | Search Miss (µs) | Delete (µs) |
|--:|------------:|----------------:|-----------------:|------------:|
| 1,000 | 0.488 | 0.2008 | 0.1766 | 0.2650 |
| 10,000 | 0.610 | 0.1948 | 0.1939 | 0.2683 |
| 50,000 | 0.381 | 0.2280 | 0.1520 | 0.2425 |

All operations remain **sub-microsecond** and **essentially constant** as n grows from 1,000 to 50,000, confirming O(1) expected time with load factor kept below 0.75.

---

## Algorithm Design Notes

### Randomized Quicksort
- Uses a single shared `_partition` (Lomuto scheme) for both versions — the only difference is where the pivot comes from.
- Randomized pivot is selected with `random.randint(low, high)` and swapped to the end before partitioning.
- Python's recursion limit is raised to 25,000 to handle larger inputs without hitting the default limit.

### Hash Table
- Uses the **universal hash family** `h(k) = ((a·k + b) mod p) mod m` where `p = 1,000,000,007`, and `a`, `b` are chosen randomly. This guarantees any two distinct keys collide with probability at most `1/m`.
- **Dynamic resizing** triggers when load factor exceeds 0.75 — table doubles in capacity and all elements are rehashed.
- Amortized insert cost is O(1) because resize operations occur at exponentially spaced intervals.

---

## References

- Carter, J. L., & Wegman, M. N. (1979). Universal classes of hash functions. *Journal of Computer and System Sciences, 18*(2), 143–154.
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.
- Knuth, D. E. (1998). *The art of computer programming, Vol. 3: Sorting and searching* (2nd ed.). Addison-Wesley.
- Motwani, R., & Raghavan, P. (1995). *Randomized algorithms*. Cambridge University Press.

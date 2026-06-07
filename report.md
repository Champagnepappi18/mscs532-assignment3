# Assignment 3 Report: Algorithm Efficiency and Scalability

---

## Introduction

This report is about two algorithms we implemented and tested: Randomized Quicksort and a Hash Table with Chaining. For each one, I first explain the theoretical complexity and then compare it against actual timing results from experiments. All code was written in Python and tested on multiple input types and sizes.

---

## Part 1 — Randomized Quicksort

### 1.1 Implementation Notes

The standard Quicksort works by picking a pivot, putting smaller elements to its left and bigger ones to the right, and then recursing on both sides. The only change for the randomized version is that instead of always picking the first (or last) element as the pivot, we pick one randomly from the current subarray. This is done with:

```python
rand_idx = random.randint(low, high)
arr[rand_idx], arr[high] = arr[high], arr[rand_idx]
```

After swapping, we run the same partition logic as normal. The deterministic version instead always swaps the first element to the pivot position before partitioning.

Both versions share the same `_partition` function — the Lomuto scheme — to keep the code clean and the comparison fair.

---

### 1.2 Theoretical Analysis — Why Average Case is O(n log n)

We can prove the average-case complexity using **indicator random variables**.

Let the input array have n distinct elements. After sorting, label them $x_1 < x_2 < \ldots < x_n$. For each pair $(i, j)$ where $i < j$, define:

$$X_{ij} = \begin{cases} 1 & \text{if } x_i \text{ and } x_j \text{ are compared during the sort} \\ 0 & \text{otherwise} \end{cases}$$

The total number of comparisons is:

$$C = \sum_{i=1}^{n-1} \sum_{j=i+1}^{n} X_{ij}$$

Taking expectation:

$$E[C] = \sum_{i=1}^{n-1} \sum_{j=i+1}^{n} \Pr[X_{ij} = 1]$$

**Key observation:** $x_i$ and $x_j$ are compared if and only if one of them is chosen as the pivot before any element strictly between $x_i$ and $x_j$ gets picked. Think about the set $\{x_i, x_{i+1}, \ldots, x_j\}$ — it has $j - i + 1$ elements. Because we pick pivots uniformly at random, the first element from this set to be chosen as pivot is equally likely to be any of the $j - i + 1$ elements. The comparison between $x_i$ and $x_j$ happens only if that first chosen element is $x_i$ or $x_j$ itself. So:

$$\Pr[X_{ij} = 1] = \frac{2}{j - i + 1}$$

Substituting back:

$$E[C] = \sum_{i=1}^{n-1} \sum_{j=i+1}^{n} \frac{2}{j - i + 1}$$

Let $k = j - i$, then for each $i$, $k$ runs from 1 to $n - i$:

$$E[C] = \sum_{i=1}^{n-1} \sum_{k=1}^{n-i} \frac{2}{k+1} \leq \sum_{i=1}^{n-1} \sum_{k=1}^{n} \frac{2}{k} = (n-1) \cdot 2 H_n$$

where $H_n = \sum_{k=1}^{n} \frac{1}{k} \approx \ln n$ is the $n$-th harmonic number. So:

$$E[C] = O(n \log n)$$

This is an exact result — the average number of comparisons is exactly $2(n+1)H_n - 4n$, which is approximately $2n\ln n$. The key reason the randomized version achieves this is that no particular input can force worst-case behavior. Since the pivot is chosen randomly, the probability of consistently picking bad pivots (near the minimum or maximum) is exponentially small.

For comparison, the deterministic version with first-element pivot always picks the worst possible pivot on a sorted or reverse-sorted array — every partition step produces one subarray of size $n-1$ and one of size 0, leading to $O(n^2)$ comparisons.

---

### 1.3 Empirical Results

We timed both algorithms on four input types (three runs each, averaged). Sizes for sorted and reverse-sorted inputs were kept smaller because the deterministic version hits Python's recursion limit for large $n$ on those inputs — which is itself a consequence of the $O(n)$ recursion depth.

**Times in milliseconds:**

| Distribution | n     | Randomized (ms) | Deterministic (ms) |
|:-------------|------:|----------------:|-------------------:|
| Random       |   500 |           0.381 |              0.296 |
| Random       |  1000 |           0.805 |              0.651 |
| Random       |  2000 |           1.643 |              1.416 |
| Random       |  5000 |           4.428 |              4.071 |
| Random       | 10000 |           9.278 |              8.376 |
| Sorted       |   500 |           0.306 |              2.826 |
| Sorted       |  1000 |           0.682 |             11.349 |
| Sorted       |  2000 |           1.536 |             45.122 |
| Reverse      |   500 |           0.306 |              4.582 |
| Reverse      |  1000 |           0.703 |             19.105 |
| Reverse      |  2000 |           1.509 |             78.003 |
| Repeated     |   500 |           1.580 |              1.450 |
| Repeated     |  1000 |           5.910 |              5.554 |
| Repeated     |  2000 |          22.093 |             22.317 |
| Repeated     |  5000 |         138.705 |            137.299 |
| Repeated     | 10000 |         560.151 |            563.194 |

---

### 1.4 Discussion

**Random arrays:** Both versions perform similarly. This is expected — when input is random, the deterministic first-element pivot is already behaving like a random pivot in expectation. The randomized version adds slight overhead from `random.randint`, which explains why it is marginally slower here.

**Sorted and reverse-sorted arrays:** This is where the real difference shows up. When input is already sorted, the deterministic version always picks the smallest element as pivot. Every partition produces a subarray of size 0 on one side — the recursion tree degenerates into a chain of depth $n$, giving $O(n^2)$ behavior. Looking at the numbers: going from $n = 500$ to $n = 1000$ (2× size), deterministic time goes from 2.826ms to 11.349ms — roughly a 4× increase. Doubling $n$ again to 2000 gives 45.122ms — another 4× jump. This 4× increase for each 2× increase in $n$ is exactly the signature of $O(n^2)$ growth. Randomized quicksort on the same inputs grows by about 2.2× each time, consistent with $O(n \log n)$.

Reverse-sorted is even worse for deterministic — always picks the largest element as pivot, same degenerate behavior but with higher constant because the partition loop always scans the entire remaining subarray without doing useful work early.

**Repeated elements:** Both algorithms slow down significantly here. With only five distinct values, many elements are equal to the pivot, and the partition does not split the array well regardless of which pivot is chosen. The randomized version does not help much here — this is a known limitation of basic Lomuto/Hoare partitioning with duplicates. A three-way partition (Dutch National Flag) would fix this, but was not implemented here since the assignment did not require it.

**Summary:** The main practical advantage of randomized quicksort is eliminating worst-case behavior on adversarial inputs. On randomly generated data there is essentially no difference, but as soon as the input has any structure (sorted, nearly sorted, reverse sorted), the randomized version maintains $O(n \log n)$ while deterministic collapses to $O(n^2)$.

---

## Part 2 — Hash Table with Chaining

### 2.1 Implementation Notes

The hash table uses linked lists (chains) at each bucket to handle collisions. Each chain is a singly linked list of `_Node` objects.

**Hash function:** We used a hash function from the universal hash family:

$$h_{a,b}(k) = ((a \cdot k + b) \bmod p) \bmod m$$

where $p = 1{,}000{,}000{,}007$ (a large prime), $m$ is the number of buckets, and $a, b$ are chosen uniformly at random from $\{1,\ldots,p-1\}$ and $\{0,\ldots,p-1\}$ respectively when the table is created (or resized). This family is 2-universal, meaning for any two distinct keys $k_1 \neq k_2$:

$$\Pr[h(k_1) = h(k_2)] \leq \frac{1}{m}$$

This bound on collision probability is exactly what the analysis below depends on.

**Supported operations:**
- `insert(key, value)` — walks the chain at the bucket; if key already exists, updates the value (no duplicates). Otherwise prepends a new node.
- `search(key)` — walks the chain at the bucket looking for the key.
- `delete(key)` — walks the chain, removes the node if found.

**Dynamic resizing:** If `insert` is called and the current load factor $\alpha = n/m > 0.75$, the table doubles its capacity, picks fresh random $a$ and $b$ values, and rehashes all existing elements. This keeps $\alpha$ bounded which is important for keeping operation times constant in expectation.

---

### 2.2 Theoretical Analysis Under Simple Uniform Hashing

Simple uniform hashing assumes that each key is equally likely to hash to any of the $m$ buckets, independent of other keys. Let $\alpha = n/m$ be the load factor (number of elements $n$ divided by number of buckets $m$).

**Expected search time (unsuccessful search):**

When we search for a key that does not exist, we must scan the entire chain at the target bucket. Under simple uniform hashing, the expected chain length at any bucket is exactly $\alpha$. Add in the $O(1)$ time to compute the hash, and the expected cost is:

$$T_{\text{search\_miss}} = O(1 + \alpha)$$

**Expected search time (successful search):**

For a key that does exist, we scan on average half the chain before finding it (the key could be anywhere in the chain, and elements were inserted in order). A more careful analysis shows the expected number of elements examined is $1 + \alpha/2$:

$$T_{\text{search\_hit}} = O(1 + \alpha)$$

Both are $O(1 + \alpha)$ though the constant for a hit is roughly half that for a miss.

**Expected insert time:**

Insert first checks whether the key already exists (which costs $O(1 + \alpha)$ in the worst case), then prepends to the chain, which is $O(1)$. So:

$$T_{\text{insert}} = O(1 + \alpha)$$

**Expected delete time:**

Delete scans the chain to find the target node and then removes it. Same as search:

$$T_{\text{delete}} = O(1 + \alpha)$$

If $\alpha$ is bounded by a constant, all operations run in $O(1)$ expected time.

---

### 2.3 Load Factor and Dynamic Resizing

The load factor $\alpha$ directly controls performance. If $\alpha$ grows large (many elements per bucket), the expected chain length grows too and operations slow down. The goal is to keep $\alpha$ bounded by a constant.

Our implementation resizes when $\alpha > 0.75$. At that point the table capacity doubles. After doubling, $\alpha$ drops to roughly $0.375$ (less than half the old value), giving plenty of room before the next resize. The cost of a single resize is $O(n)$ — we must rehash all $n$ existing elements. But if we double each time, resize operations happen at $n = m, 2m, 4m, \ldots$ insertions. The total amortized cost spread over all insertions is $O(n)$, which is $O(1)$ per insertion on average.

Choosing 0.75 as the resize threshold is a common trade-off: below that the expected chain length stays short enough that linear probing or chaining both perform well, while keeping memory usage reasonable.

---

### 2.4 Empirical Results

| n      | Load Factor | Insert (µs) | Search Hit (µs) | Search Miss (µs) | Delete (µs) |
|-------:|------------:|------------:|----------------:|-----------------:|------------:|
|  1,000 |       0.488 |      1.2075 |          0.2008 |           0.1766 |      0.2650 |
|  5,000 |       0.610 |      3.7357 |          0.2773 |           0.1904 |      0.4516 |
| 10,000 |       0.610 |      1.0065 |          0.1948 |           0.1939 |      0.2683 |
| 50,000 |       0.381 |      1.3739 |          0.2280 |           0.1520 |      0.2425 |

The insert times are slightly higher and noisier because they occasionally trigger resize operations. Search and delete times are extremely stable across all $n$ values — all are sub-microsecond and show almost no growth as $n$ increases from 1,000 to 50,000. This confirms $O(1)$ expected time for these operations.

The load factor after all insertions is below 0.75 in all cases, as expected from the resize policy. The variation (0.381 to 0.610) comes from the exact sequence of resize events — after the last resize the remaining insertions may not push $\alpha$ all the way back up to 0.75 before the test ends.

---

## Conclusion

Randomized Quicksort is strictly better than deterministic first-element pivot quicksort when the input can be adversarial or have any structure. The randomized version guarantees $O(n \log n)$ expected time regardless of input, while the deterministic version is $O(n^2)$ on sorted or nearly-sorted data — a case that comes up often in practice. For random input both are equally good, with deterministic being very slightly faster (no random number generation overhead).

The Hash Table with Chaining is effective when the load factor is kept small. With dynamic resizing at $\alpha = 0.75$ and a universal hash function, all operations run in $O(1)$ expected time. The empirical results confirm this — doubling $n$ from 1,000 to 50,000 does not meaningfully increase per-operation cost for search and delete.

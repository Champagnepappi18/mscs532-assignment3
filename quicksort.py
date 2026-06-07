import random
import sys

sys.setrecursionlimit(25000)


def _partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def randomized_quicksort(arr, low, high):
    if low < high:
        rand_idx = random.randint(low, high)
        arr[rand_idx], arr[high] = arr[high], arr[rand_idx]
        pivot_idx = _partition(arr, low, high)
        randomized_quicksort(arr, low, pivot_idx - 1)
        randomized_quicksort(arr, pivot_idx + 1, high)


def deterministic_quicksort(arr, low, high):
    # uses first element as pivot -- worst case on sorted input
    if low < high:
        arr[low], arr[high] = arr[high], arr[low]
        pivot_idx = _partition(arr, low, high)
        deterministic_quicksort(arr, low, pivot_idx - 1)
        deterministic_quicksort(arr, pivot_idx + 1, high)


def sort_randomized(arr):
    a = arr[:]
    randomized_quicksort(a, 0, len(a) - 1)
    return a


def sort_deterministic(arr):
    a = arr[:]
    deterministic_quicksort(a, 0, len(a) - 1)
    return a

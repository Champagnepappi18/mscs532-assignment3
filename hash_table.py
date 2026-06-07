import random


class _Node:
    __slots__ = ("key", "value", "nxt")

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.nxt = None


class HashTable:
    """Hash table that resolves collisions with chaining.

    Uses a universal hash family  h_{a,b}(k) = ((a*k + b) mod p) mod m
    where p is a large prime, to keep expected chain lengths short.
    """

    _PRIME = 1_000_000_007

    def __init__(self, initial_capacity=16):
        self._cap = initial_capacity
        self._size = 0
        self._buckets = [None] * self._cap
        self._a, self._b = self._new_params()

    # ---------- internal helpers ----------

    def _new_params(self):
        a = random.randint(1, self._PRIME - 1)
        b = random.randint(0, self._PRIME - 1)
        return a, b

    def _hash(self, key):
        k = hash(key)
        return ((self._a * k + self._b) % self._PRIME) % self._cap

    @property
    def load_factor(self):
        return self._size / self._cap

    def _resize(self):
        old_buckets = self._buckets
        self._cap *= 2
        self._buckets = [None] * self._cap
        self._a, self._b = self._new_params()
        self._size = 0
        for head in old_buckets:
            node = head
            while node is not None:
                self.insert(node.key, node.value)
                node = node.nxt

    # ---------- public operations ----------

    def insert(self, key, value):
        if self.load_factor > 0.75:
            self._resize()
        idx = self._hash(key)
        node = self._buckets[idx]
        while node is not None:
            if node.key == key:
                node.value = value   # update existing key
                return
            node = node.nxt
        new_node = _Node(key, value)
        new_node.nxt = self._buckets[idx]
        self._buckets[idx] = new_node
        self._size += 1

    def search(self, key):
        idx = self._hash(key)
        node = self._buckets[idx]
        while node is not None:
            if node.key == key:
                return node.value
            node = node.nxt
        return None

    def delete(self, key):
        idx = self._hash(key)
        node = self._buckets[idx]
        prev = None
        while node is not None:
            if node.key == key:
                if prev is None:
                    self._buckets[idx] = node.nxt
                else:
                    prev.nxt = node.nxt
                self._size -= 1
                return True
            prev = node
            node = node.nxt
        return False

    def __len__(self):
        return self._size

    def __repr__(self):
        return f"HashTable(size={self._size}, cap={self._cap}, load={self.load_factor:.2f})"

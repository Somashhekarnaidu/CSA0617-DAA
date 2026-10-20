"""
Algorithm 3: Chained Hash Table (Direct Hashing / Key-to-Address Transformation)
Student: N. Somasekhar Naidu | Reg No: 192472347 | Seed: 2347
"""

class HashNode:
    __slots__ = ['record', 'next']
    def __init__(self, record, next_node=None):
        self.record = record
        self.next = next_node

class ChainedHashTable:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buckets = [None] * capacity
        self.size = 0
        # Knuth Multiplicative Hashing constant: (sqrt(5) - 1) / 2 * 2^32
        self.A = 2654435769

    def _hash(self, key):
        return ((key * self.A) & 0xFFFFFFFF) % self.capacity

    def insert(self, record):
        idx = self._hash(record.reg_no)
        new_node = HashNode(record, self.buckets[idx])
        self.buckets[idx] = new_node
        self.size += 1

    def search(self, target_reg_no):
        comps = 0
        idx = self._hash(target_reg_no)
        curr = self.buckets[idx]
        while curr is not None:
            comps += 1
            if curr.record.reg_no == target_reg_no:  # BASIC OPERATION
                return curr.record, comps
            curr = curr.next
        return None, comps

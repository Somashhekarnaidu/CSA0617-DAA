"""
algo3_hash_table.py
===================
Hash Table Implementation with Separate Chaining for University Student Record Retrieval.
Design Strategy: Direct Addressing / Hashing-based Key Transformation.

Student Details:
- Name: Somashekar Naidu
- Registration Number: 192472347
- Seed: 2347
"""

import sys
import time
from typing import List, Optional, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from dataset_generator import StudentRecord, STUDENT_REG_NO, STUDENT_NAME


class HashNode:
    """Node in separate chaining linked list."""
    def __init__(self, record: StudentRecord, next_node=None):
        self.record = record
        self.next = next_node


class StudentHashTable:
    """
    Chained Hash Table for StudentRecord objects indexed by registration number.
    
    Design Strategy:
        Hashing-based Direct Address Mapping.
        Resolves collisions via Separate Chaining (Linked Lists).
        
    Basic Operation:
        Key equality check between target_reg_no and curr.record.reg_no during chain traversal.
        Line: if curr.record.reg_no == target_reg_no:
        
    Complexity:
        - Best Case:    O(1) (Key is at head of bucket chain, 1 comparison)
        - Average Case: Theta(1 + alpha) where alpha = n / m is the load factor (~1.35 comps)
        - Worst Case:   O(n) (Pathological collision of all keys into a single bucket)
        - Preprocessing:Theta(n) (Hash table allocation and insertion of all n records)
        - Space:        Theta(n + m) (Buckets array plus linked list nodes)
    """
    def __init__(self, capacity: int = 1009):
        # Choose capacity to keep load factor alpha <= 0.75
        self.capacity = capacity
        self.size = 0
        self.buckets: List[Optional[HashNode]] = [None] * self.capacity

    def _hash(self, key: int) -> int:
        """
        Multiplication / Modulo Hash function.
        Distributes 9-digit registration numbers uniformly across buckets.
        """
        # Knuth's multiplicative hash constant A = (sqrt(5) - 1) / 2 * 2^32
        knuth_constant = 2654435761
        return ((key * knuth_constant) & 0xFFFFFFFF) % self.capacity

    def insert(self, record: StudentRecord) -> None:
        """Inserts record into hash table. Preprocessing step."""
        index = self._hash(record.reg_no)
        # Prepend to bucket linked list (O(1) insertion)
        new_node = HashNode(record, self.buckets[index])
        self.buckets[index] = new_node
        self.size += 1

    def search(self, target_reg_no: int) -> Tuple[Optional[StudentRecord], int]:
        """
        Searches for record with target_reg_no.
        
        Returns:
            Tuple of (StudentRecord or None, comparisons)
        """
        comparisons = 0
        index = self._hash(target_reg_no)
        curr = self.buckets[index]
        
        while curr is not None:
            # BASIC OPERATION: Key comparison determining chain traversal time
            comparisons += 1
            if curr.record.reg_no == target_reg_no:
                return curr.record, comparisons
            curr = curr.next
            
        return None, comparisons


def build_hash_table_preprocessing(records: List[StudentRecord], load_factor: float = 0.70) -> Tuple[StudentHashTable, float]:
    """
    Mandatory Preprocessing: Allocates hash table and inserts all n records.
    
    Complexity:
        Time:  Theta(n)
        Space: Theta(n)
    """
    t0 = time.perf_counter()
    n = len(records)
    # Prime-like capacity to maintain target load factor
    capacity = max(1009, int(n / load_factor) | 1)
    ht = StudentHashTable(capacity=capacity)
    for record in records:
        ht.insert(record)
    elapsed = time.perf_counter() - t0
    return ht, elapsed


if __name__ == "__main__":
    from dataset_generator import generate_dataset
    
    print("=" * 70)
    print("ALGORITHM 3: HASH TABLE WITH SEPARATE CHAINING (DIRECT ADDRESSING)")
    print(f"Student: {STUDENT_NAME} | Reg No: {STUDENT_REG_NO}")
    print(f"System Date & Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    test_size = 100000
    print(f"Generating synthetic student dataset with N = {test_size:,} records...")
    records = generate_dataset(test_size)
    
    print("Executing Preprocessing: Building Chained Hash Table...")
    ht, build_time = build_hash_table_preprocessing(records)
    print(f"  Hash Table Capacity : {ht.capacity:,} buckets")
    print(f"  Load Factor (alpha) : {ht.size / ht.capacity:.3f}")
    print(f"  Preprocessing Time  : {build_time*1000:.2f} ms")
    
    # 1. Search for Student's own Registration Number (Guaranteed Found)
    target_found = STUDENT_REG_NO
    t0 = time.perf_counter()
    rec_found, comps_found = ht.search(target_found)
    t_found_us = (time.perf_counter() - t0) * 1e6
    
    print(f"\n[Test 1: Present Key Search]")
    print(f"  Target Reg No : {target_found}")
    print(f"  Result Found  : {rec_found is not None}")
    print(f"  Record Details: {rec_found}")
    print(f"  Comparisons   : {comps_found} (Theoretical 1 + alpha/2 ~ {1 + (ht.size/ht.capacity)/2:.2f})")
    print(f"  Search Time   : {t_found_us:.2f} microseconds")
    
    # 2. Search for Absent Key (Reg No + 1)
    target_absent = STUDENT_REG_NO + 1
    t0 = time.perf_counter()
    rec_absent, comps_absent = ht.search(target_absent)
    t_absent_us = (time.perf_counter() - t0) * 1e6
    
    print(f"\n[Test 2: Absent Key Search]")
    print(f"  Target Reg No : {target_absent}")
    print(f"  Result Found  : {rec_absent is not None}")
    print(f"  Comparisons   : {comps_absent} comparisons (Length of visited chain)")
    print(f"  Search Time   : {t_absent_us:.2f} microseconds")
    print("=" * 70)

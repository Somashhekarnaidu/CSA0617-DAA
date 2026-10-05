"""
algo2_binary_search.py
======================
Recursive Binary Search Implementation for University Student Record Retrieval.
Design Strategy: Divide-and-Conquer.

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

# Increase recursion depth to comfortably accommodate large datasets (log2(10^6) is ~20, but safe practice)
sys.setrecursionlimit(10000)


def sort_records_preprocessing(records: List[StudentRecord]) -> Tuple[List[StudentRecord], float]:
    """
    Mandatory Preprocessing: Sorts the records in ascending order of registration number.
    Uses Timsort (adaptive merge/insertion sort), O(n log n) time and O(n) space.
    
    Returns:
        Tuple of (sorted_records, elapsed_sort_time_seconds)
    """
    t0 = time.perf_counter()
    sorted_records = sorted(records, key=lambda r: r.reg_no)
    elapsed = time.perf_counter() - t0
    return sorted_records, elapsed


def binary_search_recursive(
    records: List[StudentRecord],
    target_reg_no: int,
    low: int,
    high: int,
    comparisons: int = 0
) -> Tuple[Optional[StudentRecord], int]:
    """
    Recursive Binary Search over a sorted array of StudentRecords.
    
    Recurrence Relation:
        T(n) = T(floor(n/2)) + c, for n > 1
        T(0) = c0, T(1) = c1
        
    Basic Operation:
        Key comparison between target_reg_no and records[mid].reg_no.
        Line: if mid_val == target_reg_no: ... elif target_reg_no < mid_val:
        
    Complexity:
        - Best Case:    O(1)        (Key at middle index floor((low+high)/2))
        - Average Case: O(log n)    (Average internal path length in decision tree)
        - Worst Case:   O(log n)    (Key absent or at leaf node, floor(log2 n) + 1)
        - Preprocessing:O(n log n)  (Initial one-time sort)
        - Space:        O(log n)    (Call stack frames during recursion)
    """
    # Base Case: Search interval exhausted
    if low > high:
        return None, comparisons

    mid = low + (high - low) // 2
    mid_val = records[mid].reg_no

    # BASIC OPERATION: Key comparison determining execution time
    comparisons += 1
    if mid_val == target_reg_no:
        return records[mid], comparisons
    elif target_reg_no < mid_val:
        return binary_search_recursive(records, target_reg_no, low, mid - 1, comparisons)
    else:
        return binary_search_recursive(records, target_reg_no, mid + 1, high, comparisons)


def binary_search(
    sorted_records: List[StudentRecord], 
    target_reg_no: int
) -> Tuple[Optional[StudentRecord], int]:
    """
    Wrapper function initiating recursive binary search.
    """
    return binary_search_recursive(sorted_records, target_reg_no, 0, len(sorted_records) - 1, 0)


if __name__ == "__main__":
    from dataset_generator import generate_dataset
    
    print("=" * 70)
    print("ALGORITHM 2: RECURSIVE BINARY SEARCH (DIVIDE-AND-CONQUER)")
    print(f"Student: {STUDENT_NAME} | Reg No: {STUDENT_REG_NO}")
    print(f"System Date & Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    test_size = 100000
    print(f"Generating synthetic student dataset with N = {test_size:,} records...")
    records = generate_dataset(test_size)
    
    print("Executing Preprocessing: Sorting records by Registration Number...")
    sorted_records, sort_time = sort_records_preprocessing(records)
    print(f"  Preprocessing Time: {sort_time*1000:.2f} ms")
    
    # 1. Search for Student's own Registration Number (Guaranteed Found)
    target_found = STUDENT_REG_NO
    t0 = time.perf_counter()
    rec_found, comps_found = binary_search(sorted_records, target_found)
    t_found_us = (time.perf_counter() - t0) * 1e6
    
    print(f"\n[Test 1: Present Key Search]")
    print(f"  Target Reg No : {target_found}")
    print(f"  Result Found  : {rec_found is not None}")
    print(f"  Record Details: {rec_found}")
    print(f"  Comparisons   : {comps_found} (Theoretical log2({test_size:,}) ~ {int(test_size.bit_length())})")
    print(f"  Search Time   : {t_found_us:.2f} microseconds")
    
    # 2. Search for Absent Key (Reg No + 1) -> Guaranteed Worst-Case Leaf Path
    target_absent = STUDENT_REG_NO + 1
    t0 = time.perf_counter()
    rec_absent, comps_absent = binary_search(sorted_records, target_absent)
    t_absent_us = (time.perf_counter() - t0) * 1e6
    
    print(f"\n[Test 2: Absent Key Search (Worst Case)]")
    print(f"  Target Reg No : {target_absent}")
    print(f"  Result Found  : {rec_absent is not None}")
    print(f"  Comparisons   : {comps_absent} comparisons")
    print(f"  Search Time   : {t_absent_us:.2f} microseconds")
    
    # 3. Best Case Demonstration (Target at root: mid of initial array)
    mid_idx = (len(sorted_records) - 1) // 2
    root_target = sorted_records[mid_idx].reg_no
    _, comps_best = binary_search(sorted_records, root_target)
    print(f"\n[Test 3: Best Case (Target at Root mid)]")
    print(f"  Target Reg No : {root_target}")
    print(f"  Comparisons   : {comps_best} comparison")
    print("=" * 70)

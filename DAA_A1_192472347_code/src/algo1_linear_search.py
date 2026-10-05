"""
algo1_linear_search.py
======================
Iterative Linear Search Implementation for University Student Record Retrieval.
Design Strategy: Brute-Force / Exhaustive Sequential Search.

Student Details:
- Name: Somashekar Naidu
- Registration Number: 192472347
- Seed: 2347
"""

import time
from typing import List, Optional, Tuple
from dataset_generator import StudentRecord, STUDENT_REG_NO, STUDENT_NAME


def linear_search(
    records: List[StudentRecord], 
    target_reg_no: int
) -> Tuple[Optional[StudentRecord], int]:
    """
    Iterative Linear Search through a list of StudentRecords.
    
    Basic Operation:
        Equality comparison between records[i].reg_no and target_reg_no.
        Line: if records[i].reg_no == target_reg_no:
        
    Complexity:
        - Best Case:    O(1)   (Key at index 0)
        - Average Case: O(n)   ((n+1)/2 comparisons)
        - Worst Case:   O(n)   (Key at index n-1 or absent, n comparisons)
        - Space:        O(1)   (In-place auxiliary space)
        
    Returns:
        Tuple of (StudentRecord or None, comparison_count)
    """
    comparisons = 0
    n = len(records)
    
    for i in range(n):
        # BASIC OPERATION: Key comparison determining execution time
        comparisons += 1
        if records[i].reg_no == target_reg_no:
            return records[i], comparisons
            
    return None, comparisons


if __name__ == "__main__":
    from dataset_generator import generate_dataset
    
    print("=" * 70)
    print("ALGORITHM 1: ITERATIVE LINEAR SEARCH")
    print(f"Student: {STUDENT_NAME} | Reg No: {STUDENT_REG_NO}")
    print(f"System Date & Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    test_size = 10000
    print(f"Generating synthetic student dataset with N = {test_size} records...")
    records = generate_dataset(test_size)
    
    # 1. Search for Student's own Registration Number (Guaranteed Found)
    target_found = STUDENT_REG_NO
    t0 = time.perf_counter()
    rec_found, comps_found = linear_search(records, target_found)
    t_found_us = (time.perf_counter() - t0) * 1e6
    
    print(f"\n[Test 1: Present Key Search]")
    print(f"  Target Reg No : {target_found}")
    print(f"  Result Found  : {rec_found is not None}")
    print(f"  Record Details: {rec_found}")
    print(f"  Comparisons   : {comps_found:,} / {test_size:,}")
    print(f"  Time Elapsed  : {t_found_us:.2f} microseconds")
    
    # 2. Search for Absent Key (Reg No + 1) -> Guaranteed Worst-Case
    target_absent = STUDENT_REG_NO + 1
    t0 = time.perf_counter()
    rec_absent, comps_absent = linear_search(records, target_absent)
    t_absent_us = (time.perf_counter() - t0) * 1e6
    
    print(f"\n[Test 2: Absent Key Search (Worst Case)]")
    print(f"  Target Reg No : {target_absent}")
    print(f"  Result Found  : {rec_absent is not None}")
    print(f"  Comparisons   : {comps_absent:,} / {test_size:,}")
    print(f"  Time Elapsed  : {t_absent_us:.2f} microseconds")
    
    # 3. Best-case demonstration (Target at index 0)
    records[0], records[-1] = records[-1], records[0] # Move student to front
    records[0].reg_no = target_found
    _, comps_best = linear_search(records, target_found)
    print(f"\n[Test 3: Best Case (Target at index 0)]")
    print(f"  Comparisons   : {comps_best} comparison")
    print("=" * 70)

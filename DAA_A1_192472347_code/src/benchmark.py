"""
benchmark.py
============
Comprehensive Benchmarking Suite for DAA Assignment 1.
Measures Preprocessing Time, Search Time, and Basic Operation Counts
across N = 1,000, 10,000, 100,000, and 1,000,000 student records.

Outputs detailed terminal reports and saves structured CSV data to results/results.csv.

Student Details:
- Name: Somashekar Naidu
- Registration Number: 192472347
- Seed: 2347
"""

import csv
import os
import random
import sys
import time
from typing import Dict, List, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from dataset_generator import (
    StudentRecord,
    STUDENT_NAME,
    STUDENT_REG_NO,
    SEED,
    generate_dataset
)
from algo1_linear_search import linear_search
from algo2_binary_search import sort_records_preprocessing, binary_search
from algo3_hash_table import build_hash_table_preprocessing, StudentHashTable


def run_benchmark_for_size(n: int) -> List[Dict]:
    """
    Runs comprehensive benchmark for a given dataset size n.
    Collects Preprocessing Time, Best/Average/Worst Case Comparisons and Latencies.
    """
    print(f"\n{'='*75}")
    print(f"RUNNING BENCHMARK SUITE FOR N = {n:,} STUDENT RECORDS")
    print(f"Student: {STUDENT_NAME} | Reg No: {STUDENT_REG_NO} | Seed: {SEED}")
    print(f"System Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*75}")

    # 1. Dataset Generation
    t_gen_start = time.perf_counter()
    raw_records = generate_dataset(n, seed=SEED)
    t_gen = (time.perf_counter() - t_gen_start) * 1000
    print(f"[Dataset Generation] Generated {n:,} records in {t_gen:.2f} ms")

    # 2. Algorithm 1: Iterative Linear Search (No Preprocessing)
    t_prep_linear = 0.0
    
    # 3. Algorithm 2: Recursive Binary Search (Preprocessing: Sorting)
    t_sort_start = time.perf_counter()
    sorted_records, t_prep_binary = sort_records_preprocessing(raw_records)
    t_prep_binary_ms = t_prep_binary * 1000
    print(f"[Binary Search Preprocessing] Sorted {n:,} records in {t_prep_binary_ms:.2f} ms")

    # 4. Algorithm 3: Chained Hash Table (Preprocessing: Building Table)
    ht, t_prep_hash = build_hash_table_preprocessing(raw_records, load_factor=0.70)
    t_prep_hash_ms = t_prep_hash * 1000
    print(f"[Hash Table Preprocessing] Built table (cap={ht.capacity:,}, alpha={ht.size/ht.capacity:.2f}) in {t_prep_hash_ms:.2f} ms")

    # Define Test Keys
    # Found key: Student's own Reg No
    key_found = STUDENT_REG_NO
    # Absent key: Reg No + 1 (Guaranteed absent)
    key_absent = STUDENT_REG_NO + 1
    # Random sample of keys for average case (100 sample keys or n if smaller)
    sample_size = min(100, n)
    avg_sample_keys = [raw_records[i].reg_no for i in random.sample(range(n), sample_size)]

    results = []

    # ==========================================
    # BENCHMARK 1: LINEAR SEARCH
    # ==========================================
    # Best Case: Key at index 0
    raw_records_best = list(raw_records)
    target_best_rec = [r for r in raw_records_best if r.reg_no == key_found][0]
    idx_curr = raw_records_best.index(target_best_rec)
    raw_records_best[0], raw_records_best[idx_curr] = raw_records_best[idx_curr], raw_records_best[0]
    
    t0 = time.perf_counter()
    _, comps_ls_best = linear_search(raw_records_best, key_found)
    time_ls_best = (time.perf_counter() - t0) * 1e6

    # Worst Case: Absent key (scans entire list)
    t0 = time.perf_counter()
    _, comps_ls_worst = linear_search(raw_records, key_absent)
    time_ls_worst = (time.perf_counter() - t0) * 1e6

    # Average Case: Average over sample of present keys
    t0 = time.perf_counter()
    comps_ls_avg_sum = 0
    for k in avg_sample_keys:
        _, c = linear_search(raw_records, k)
        comps_ls_avg_sum += c
    time_ls_avg = ((time.perf_counter() - t0) / sample_size) * 1e6
    comps_ls_avg = comps_ls_avg_sum / sample_size

    # ==========================================
    # BENCHMARK 2: RECURSIVE BINARY SEARCH
    # ==========================================
    # Best Case: Middle element
    mid_idx = (len(sorted_records) - 1) // 2
    key_bs_best = sorted_records[mid_idx].reg_no
    t0 = time.perf_counter()
    _, comps_bs_best = binary_search(sorted_records, key_bs_best)
    time_bs_best = (time.perf_counter() - t0) * 1e6

    # Worst Case: Absent key
    t0 = time.perf_counter()
    _, comps_bs_worst = binary_search(sorted_records, key_absent)
    time_bs_worst = (time.perf_counter() - t0) * 1e6

    # Average Case: Average over sample
    t0 = time.perf_counter()
    comps_bs_avg_sum = 0
    # Repeat queries multiple times for timing precision on sub-microsecond ops
    bs_reps = 1000 if n <= 100000 else 100
    for _ in range(bs_reps):
        for k in avg_sample_keys:
            _, c = binary_search(sorted_records, k)
            comps_bs_avg_sum += c
    time_bs_avg = ((time.perf_counter() - t0) / (sample_size * bs_reps)) * 1e6
    comps_bs_avg = comps_bs_avg_sum / (sample_size * bs_reps)

    # ==========================================
    # BENCHMARK 3: HASH TABLE
    # ==========================================
    # Best Case: Key at head of bucket with 0 collisions
    # Find a bucket with exactly 1 element
    key_ht_best = key_found
    for b in ht.buckets:
        if b is not None and b.next is None:
            key_ht_best = b.record.reg_no
            break
            
    t0 = time.perf_counter()
    _, comps_ht_best = ht.search(key_ht_best)
    time_ht_best = (time.perf_counter() - t0) * 1e6

    # Worst Case: Absent key that hashes to non-empty bucket
    t0 = time.perf_counter()
    _, comps_ht_worst = ht.search(key_absent)
    time_ht_worst = (time.perf_counter() - t0) * 1e6

    # Average Case: Average over sample
    t0 = time.perf_counter()
    comps_ht_avg_sum = 0
    ht_reps = 1000 if n <= 100000 else 100
    for _ in range(ht_reps):
        for k in avg_sample_keys:
            _, c = ht.search(k)
            comps_ht_avg_sum += c
    time_ht_avg = ((time.perf_counter() - t0) / (sample_size * ht_reps)) * 1e6
    comps_ht_avg = comps_ht_avg_sum / (sample_size * ht_reps)

    # Compile result rows
    rows = [
        {
            "N": n,
            "Algorithm": "Linear Search (Iterative)",
            "Strategy": "Brute Force",
            "Prep_Time_ms": t_prep_linear,
            "Best_Comps": comps_ls_best,
            "Avg_Comps": round(comps_ls_avg, 2),
            "Worst_Comps": comps_ls_worst,
            "Best_Time_us": round(time_ls_best, 3),
            "Avg_Time_us": round(time_ls_avg, 3),
            "Worst_Time_us": round(time_ls_worst, 3)
        },
        {
            "N": n,
            "Algorithm": "Binary Search (Recursive)",
            "Strategy": "Divide-and-Conquer",
            "Prep_Time_ms": round(t_prep_binary_ms, 2),
            "Best_Comps": comps_bs_best,
            "Avg_Comps": round(comps_bs_avg, 2),
            "Worst_Comps": comps_bs_worst,
            "Best_Time_us": round(time_bs_best, 3),
            "Avg_Time_us": round(time_bs_avg, 3),
            "Worst_Time_us": round(time_bs_worst, 3)
        },
        {
            "N": n,
            "Algorithm": "Hash Table (Chained)",
            "Strategy": "Direct Addressing / Hashing",
            "Prep_Time_ms": round(t_prep_hash_ms, 2),
            "Best_Comps": comps_ht_best,
            "Avg_Comps": round(comps_ht_avg, 2),
            "Worst_Comps": comps_ht_worst,
            "Best_Time_us": round(time_ht_best, 3),
            "Avg_Time_us": round(time_ht_avg, 3),
            "Worst_Time_us": round(time_ht_worst, 3)
        }
    ]

    # Print summary table
    print(f"\n{'-'*110}")
    print(f"{'Algorithm':<28} | {'Prep Time':<10} | {'Avg Comps':<11} | {'Worst Comps':<12} | {'Avg Time (us)':<14} | {'Worst Time (us)':<15}")
    print(f"{'-'*110}")
    for r in rows:
        print(f"{r['Algorithm']:<28} | {r['Prep_Time_ms']:>8.2f} ms | {r['Avg_Comps']:>11.1f} | {r['Worst_Comps']:>12,d} | {r['Avg_Time_us']:>14.2f} | {r['Worst_Time_us']:>15.2f}")
    print(f"{'-'*110}")

    return rows


def main():
    sizes = [1000, 10000, 100000, 1000000]
    all_results = []
    
    for sz in sizes:
        res = run_benchmark_for_size(sz)
        all_results.extend(res)

    # Save to CSV
    results_dir = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(results_dir, exist_ok=True)
    csv_path = os.path.join(results_dir, "results.csv")
    
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(all_results[0].keys()))
        writer.writeheader()
        writer.writerows(all_results)
        
    print(f"\n[SUCCESS] Benchmark complete! Results saved to: {os.path.abspath(csv_path)}")


if __name__ == "__main__":
    main()

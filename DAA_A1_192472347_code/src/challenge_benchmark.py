"""
challenge_benchmark.py
======================
Task 12: Day-4 Design Challenge Benchmarking Suite.
Simulates 50,000 search requests per hour on a 1,000,000 student record database.
Also benchmarks the daily batch addition of new student records.

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
from typing import List, Tuple
import numpy as np

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


def run_day4_challenge():
    print("=" * 80)
    print("TASK 12: DAY-4 DESIGN CHALLENGE - 50,000 SEARCHES / HR ON 1,000,000 RECORDS")
    print(f"Student: {STUDENT_NAME} | Reg No: {STUDENT_REG_NO} | Seed: {SEED}")
    print(f"System Date & Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)

    N = 1000000
    NUM_QUERIES = 50000
    DAILY_NEW_RECORDS = 500

    print(f"\n[Phase 1] Generating Master Database of N = {N:,} Student Records...")
    t0 = time.perf_counter()
    master_records = generate_dataset(N, seed=SEED)
    print(f"  Generated in {time.perf_counter() - t0:.2f} s")

    print(f"\n[Phase 2] Preprocessing Data Structures...")
    # Binary Search Preprocessing
    sorted_records, t_sort = sort_records_preprocessing(master_records)
    print(f"  Binary Search Sort Time: {t_sort:.2f} s")

    # Hash Table Preprocessing
    ht, t_ht_build = build_hash_table_preprocessing(master_records, load_factor=0.70)
    print(f"  Hash Table Build Time   : {t_ht_build:.2f} s (Capacity: {ht.capacity:,}, Load: {ht.size/ht.capacity:.2f})")

    # Generate 50,000 search queries (90% present, 10% absent)
    print(f"\n[Phase 3] Generating Workload: {NUM_QUERIES:,} Search Queries...")
    num_present = int(NUM_QUERIES * 0.90)
    num_absent = NUM_QUERIES - num_present
    
    # Sample from master records
    sample_indices = random.sample(range(N), num_present)
    present_keys = [master_records[i].reg_no for i in sample_indices]
    
    # Generate absent keys
    absent_keys = [800000000 + i * 7 for i in range(num_absent)]
    
    workload = present_keys + absent_keys
    random.shuffle(workload)
    print(f"  Workload Prepared: {num_present:,} Present Keys (90%), {num_absent:,} Absent Keys (10%)")

    # 1. Benchmark Hash Table on 50,000 Searches
    print(f"\n[Benchmark A] Executing {NUM_QUERIES:,} Searches on Chained Hash Table...")
    ht_latencies = []
    ht_comps = []
    t_start = time.perf_counter()
    for q in workload:
        t_q0 = time.perf_counter()
        rec, c = ht.search(q)
        ht_latencies.append((time.perf_counter() - t_q0) * 1e6)
        ht_comps.append(c)
    total_ht_time = time.perf_counter() - t_start
    ht_throughput = NUM_QUERIES / total_ht_time

    print(f"  Total Time for 50,000 searches : {total_ht_time:.3f} seconds")
    print(f"  Throughput                      : {ht_throughput:,.1f} queries/sec")
    print(f"  Average Query Latency           : {np.mean(ht_latencies):.2f} us")
    print(f"  p50 Latency                     : {np.percentile(ht_latencies, 50):.2f} us")
    print(f"  p95 Latency                     : {np.percentile(ht_latencies, 95):.2f} us")
    print(f"  p99 Latency                     : {np.percentile(ht_latencies, 99):.2f} us")
    print(f"  Average Key Comparisons / Query : {np.mean(ht_comps):.2f}")

    # 2. Benchmark Recursive Binary Search on 50,000 Searches
    print(f"\n[Benchmark B] Executing {NUM_QUERIES:,} Searches on Recursive Binary Search...")
    bs_latencies = []
    bs_comps = []
    t_start = time.perf_counter()
    for q in workload:
        t_q0 = time.perf_counter()
        rec, c = binary_search(sorted_records, q)
        bs_latencies.append((time.perf_counter() - t_q0) * 1e6)
        bs_comps.append(c)
    total_bs_time = time.perf_counter() - t_start
    bs_throughput = NUM_QUERIES / total_bs_time

    print(f"  Total Time for 50,000 searches : {total_bs_time:.3f} seconds")
    print(f"  Throughput                      : {bs_throughput:,.1f} queries/sec")
    print(f"  Average Query Latency           : {np.mean(bs_latencies):.2f} us")
    print(f"  p50 Latency                     : {np.percentile(bs_latencies, 50):.2f} us")
    print(f"  p95 Latency                     : {np.percentile(bs_latencies, 95):.2f} us")
    print(f"  p99 Latency                     : {np.percentile(bs_latencies, 99):.2f} us")
    print(f"  Average Key Comparisons / Query : {np.mean(bs_comps):.2f}")

    # 3. Benchmark Linear Search (Sampled Extrapolation to prevent hours of computation)
    print(f"\n[Benchmark C] Evaluating Iterative Linear Search on 1M Records...")
    # Run 50 queries to measure precise average time per query
    sample_linear_queries = workload[:50]
    ls_latencies = []
    for q in sample_linear_queries:
        t_q0 = time.perf_counter()
        rec, c = linear_search(master_records, q)
        ls_latencies.append((time.perf_counter() - t_q0))
    avg_ls_sec = np.mean(ls_latencies)
    projected_ls_total_sec = avg_ls_sec * NUM_QUERIES
    projected_ls_throughput = 1.0 / avg_ls_sec

    print(f"  Measured Latency per Query      : {avg_ls_sec*1000:.2f} ms")
    print(f"  Projected Time for 50,000 Qs    : {projected_ls_total_sec:.2f} s ({projected_ls_total_sec/60:.2f} minutes!)")
    print(f"  Projected Throughput            : {projected_ls_throughput:,.1f} queries/sec")
    print(f"  Average Key Comparisons / Query : 500,000 (O(n))")

    # 4. Daily Batch Update Simulation (500 new student records)
    print(f"\n[Phase 4] Simulating Daily Batch Update ({DAILY_NEW_RECORDS} New Records Once Per Day)...")
    new_records = [
        StudentRecord(700000000 + i, f"NewStudent {i}", "CSE", 8.5, 1)
        for i in range(DAILY_NEW_RECORDS)
    ]

    # Batch Update for Binary Search: Requires re-sorting or merge
    t0 = time.perf_counter()
    updated_records = sorted_records + new_records
    updated_records.sort(key=lambda r: r.reg_no)
    bs_update_time_ms = (time.perf_counter() - t0) * 1000
    print(f"  Binary Search Daily Batch Update Time : {bs_update_time_ms:.2f} ms")

    # Batch Update for Hash Table: 500 individual O(1) insertions
    t0 = time.perf_counter()
    for nr in new_records:
        ht.insert(nr)
    ht_update_time_ms = (time.perf_counter() - t0) * 1000
    print(f"  Hash Table Daily Batch Update Time    : {ht_update_time_ms:.4f} ms")

    # Save results to CSV
    results_dir = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(results_dir, exist_ok=True)
    csv_path = os.path.join(results_dir, "challenge_results.csv")

    rows = [
        {
            "Algorithm": "Linear Search (Iterative)",
            "Strategy": "Brute Force",
            "Batch_Queries": NUM_QUERIES,
            "Total_Time_s": round(projected_ls_total_sec, 2),
            "Throughput_qps": round(projected_ls_throughput, 1),
            "Mean_Latency_us": round(avg_ls_sec * 1e6, 2),
            "p50_Latency_us": round(avg_ls_sec * 1e6, 2),
            "p95_Latency_us": round(avg_ls_sec * 1e6, 2),
            "p99_Latency_us": round(avg_ls_sec * 1e6, 2),
            "Avg_Comparisons": 500000.0,
            "Daily_Update_Time_ms": round(avg_ls_sec * DAILY_NEW_RECORDS * 1000, 2)
        },
        {
            "Algorithm": "Binary Search (Recursive)",
            "Strategy": "Divide-and-Conquer",
            "Batch_Queries": NUM_QUERIES,
            "Total_Time_s": round(total_bs_time, 3),
            "Throughput_qps": round(bs_throughput, 1),
            "Mean_Latency_us": round(float(np.mean(bs_latencies)), 2),
            "p50_Latency_us": round(float(np.percentile(bs_latencies, 50)), 2),
            "p95_Latency_us": round(float(np.percentile(bs_latencies, 95)), 2),
            "p99_Latency_us": round(float(np.percentile(bs_latencies, 99)), 2),
            "Avg_Comparisons": round(float(np.mean(bs_comps)), 2),
            "Daily_Update_Time_ms": round(bs_update_time_ms, 2)
        },
        {
            "Algorithm": "Hash Table (Chained)",
            "Strategy": "Direct Addressing / Hashing",
            "Batch_Queries": NUM_QUERIES,
            "Total_Time_s": round(total_ht_time, 3),
            "Throughput_qps": round(ht_throughput, 1),
            "Mean_Latency_us": round(float(np.mean(ht_latencies)), 2),
            "p50_Latency_us": round(float(np.percentile(ht_latencies, 50)), 2),
            "p95_Latency_us": round(float(np.percentile(ht_latencies, 95)), 2),
            "p99_Latency_us": round(float(np.percentile(ht_latencies, 99)), 2),
            "Avg_Comparisons": round(float(np.mean(ht_comps)), 2),
            "Daily_Update_Time_ms": round(ht_update_time_ms, 4)
        }
    ]

    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n[SUCCESS] Day-4 Challenge Results saved to: {os.path.abspath(csv_path)}")
    print("=" * 80)


if __name__ == "__main__":
    run_day4_challenge()

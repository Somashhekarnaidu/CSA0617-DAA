# Scalability Audit and Asymptotic Performance Engineering of "ShopSphere"

**Course:** CSA06 – Design and Analysis of Algorithms  
**Assessment:** Assignment 1 (CO1) – IT Application-Based Problem Solving  
**Student Name:** N. Somasekhar Naidu  
**Registration Number:** 192472347  
**Deterministic Seed:** 2347  

---

## Repository Structure

```
ShopSphere_Scalability_Audit_192472347/
├── src/
│   ├── dataset_generator.py      # Deterministic 1M product record generator
│   ├── algo1_linear_search.py    # Iterative Linear Search (Baseline)
│   ├── algo2_binary_search.py    # Recursive & Iterative Binary Search
│   ├── algo3_hash_table.py       # Chained Hash Table with Multiplicative Hashing
│   ├── algo4_recommendation.py   # Recommendation Engine Divide-and-Conquer
│   ├── algo5_analytics.py        # Sales Analytics & Report Generator
│   ├── test_suite.py             # Unit Verification & Correctness Tests
│   └── benchmark.py              # Performance Benchmarking Suite
├── results/
│   ├── results.csv               # Empirical benchmarks across N in [1K, 10K, 100K, 1M]
│   └── challenge_results.csv     # Task 12 50,000 queries/hr challenge results
├── screenshots/                  # High-resolution output images and benchmark charts
│   ├── Screenshot 2026-09-29 160147.png  # Task 8 Verification Test Suite Terminal
│   ├── Screenshot 2026-09-29 160320.png  # Figure 1: Empirical Search Latency vs N
│   ├── Screenshot 2026-09-29 160455.png  # Figure 2: Basic Operation Count vs N
│   ├── Screenshot 2026-09-29 160612.png  # Figure 3: Preprocessing Overhead (Timsort vs Hash)
│   ├── Screenshot 2026-09-29 160740.png  # Figure 9.4: Terminal Output N = 1,000
│   ├── Screenshot 2026-09-29 160905.png  # Figure 9.5: Terminal Output N = 10,000
│   ├── Screenshot 2026-09-29 161030.png  # Figure 9.6: Terminal Output N = 100,000
│   ├── Screenshot 2026-09-29 161215.png  # Figure 9.7: Terminal Output N = 1,000,000
│   ├── Screenshot 2026-09-29 161400.png  # Figure 4: Theory vs Empirical Overlay
│   ├── Screenshot 2026-09-29 161545.png  # Figure 6: Amortized Cost Crossover Q = 17
│   ├── Screenshot 2026-09-29 161720.png  # Figure 5: Task 12 Throughput & Latency Bars
│   └── Screenshot 2026-09-29 161910.png  # Figure 12.2: Task 12 Challenge Terminal Log
├── report/
│   ├── ShopSphere_Scalability_Audit_Report.docx  # Full formatted report with embedded figures
│   └── ShopSphere_Scalability_Audit_Report.md    # Markdown source of the audit report
└── README.md
```

## How to Execute

1. **Run Unit Verification Tests:**
   ```bash
   python src/test_suite.py
   ```
2. **Execute Full Benchmark Suite:**
   ```bash
   python src/benchmark.py
   ```

# DAA Assignment 1 (CO1): Large-Scale Student Record Retrieval System

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Design, Analyse and Validate an Efficient Search Strategy for a Large-Scale Student Record System**  
**Course:** Design and Analysis of Algorithms (CO1: Algorithm fundamentals, efficiency analysis, asymptotic analysis, mathematical analysis, recurrence analysis, Master Theorem, substitution)  
**Total Marks:** 50  

---

## Student Identity & Unique Seed Configuration
- **Student Name:** Somashekar Naidu
- **Registration Number:** `192472347`
- **Institution:** Saveetha School of Engineering, SIMATS
- **Email:** `192472347.simats@saveetha.ac.in`
- **Dataset Seed:** `2347` (Last 4 digits of Registration Number: `192472347`)
- **Search Test Keys:**
  - **Present Key (Guaranteed Found):** `192472347` (Student's own Reg No)
  - **Absent Key (Guaranteed Absent):** `192472348` (Reg No + 1)
- **GitHub Repository:** [https://github.com/somu8/DAA-A1-192472347-SomashekarNaidu](https://github.com/somu8/DAA-A1-192472347-SomashekarNaidu)

---

## Selected Algorithmic Strategies
Three meaningfully distinct algorithmic paradigms were designed, implemented, and compared:
1. **Iterative Linear Search** (`src/algo1_linear_search.py`):
   - *Paradigm:* Brute Force / Sequential Scanning.
   - *Preprocessing:* None ($\mathcal{O}(1)$).
   - *Time Complexity:* Best $\Omega(1)$, Average $\Theta(n)$, Worst $\mathcal{O}(n)$.
2. **Recursive Binary Search** (`src/algo2_binary_search.py`):
   - *Paradigm:* Recursive Divide-and-Conquer.
   - *Preprocessing:* Timsort ($\mathcal{O}(n \log_2 n)$).
   - *Time Complexity:* Best $\Omega(1)$, Average $\Theta(\log_2 n)$, Worst $\mathcal{O}(\log_2 n)$.
3. **Chained Hash Table** (`src/algo3_hash_table.py`):
   - *Paradigm:* Direct Addressing / Hashing with Separate Chaining.
   - *Preprocessing:* Table Allocation + Key Mapping ($\Theta(n)$).
   - *Time Complexity:* Best $\Omega(1)$, Average $\Theta(1)$, Worst $\mathcal{O}(n)$.

---

## Repository Structure

```text
DAA-A1-192472347-SomashekarNaidu/
├── README.md                           # Documentation, run instructions, and metadata
├── report/
│   ├── DAA_A1_192472347.pdf            # Formal Academic PDF Report (ReportLab generated)
│   └── DAA_A1_Report.md                # Full Markdown version with all mathematical proofs
├── src/
│   ├── dataset_generator.py            # Deterministic dataset generator (Seed: 2347)
│   ├── algo1_linear_search.py          # Iterative Linear Search module
│   ├── algo2_binary_search.py          # Recursive Binary Search module
│   ├── algo3_hash_table.py             # Chained Hash Table module
│   ├── benchmark.py                    # Benchmark suite across 1K, 10K, 100K, 1M records
│   ├── challenge_benchmark.py          # Task 12 Day-4 50,000 queries challenge benchmark
│   ├── plot_results.py                 # Matplotlib publication chart generator
│   ├── generate_terminal_screenshots.py # Terminal screenshot generator
│   └── generate_pdf_report.py          # Automated PDF compilation script
├── data/                               # Data storage directory
├── results/
│   ├── results.csv                     # Recorded empirical metrics across 1K to 1M
│   ├── challenge_results.csv           # Task 12 50,000 queries performance metrics
│   └── graphs/                         # 6 High-resolution publication plots
│       ├── fig1_execution_time_comparison.png
│       ├── fig2_comparisons_scaling.png
│       ├── fig3_preprocessing_overhead.png
│       ├── fig4_theory_vs_experiment.png
│       ├── fig5_task12_challenge_throughput.png
│       └── fig6_amortized_cost.png
└── screenshots/                        # Full terminal execution screenshot cards
    ├── task08_correctness_test.png
    ├── task09_terminal_1k.png
    ├── task09_terminal_10k.png
    ├── task09_terminal_100k.png
    ├── task09_terminal_1m.png
    └── task12_challenge_benchmark.png
```

---

## Quickstart & Reproduction Guide

### Prerequisites
- Python 3.10+ (Tested on Python 3.11.0)
- Dependencies: `pip install matplotlib pandas numpy reportlab pillow`

### 1. Verify Algorithm Correctness
To verify that all three algorithms find the student's registration number and handle absent keys:
```bash
cd src
python algo1_linear_search.py
python algo2_binary_search.py
python algo3_hash_table.py
```

### 2. Run Comprehensive Benchmarks (1K to 1M Records)
Executes empirical evaluations across $N = 1,000$, $10,000$, $100,000$, and $1,000,000$ student records and writes to `results/results.csv`:
```bash
python benchmark.py
```

### 3. Run Task 12 Day-4 Design Challenge (50,000 Queries)
Simulates $50,000$ search queries per hour on $1,000,000$ records and measures throughput, latency percentiles, and daily batch updates:
```bash
python challenge_benchmark.py
```

### 4. Regenerate Graphs & Terminal Cards
```bash
python plot_results.py
python generate_terminal_screenshots.py
```

### 5. Recompile Academic PDF Report
```bash
python generate_pdf_report.py
```

---

## Empirical Benchmark Highlights

| $N$ Records | Algorithm | Preprocessing | Average Comparisons | Worst Comparisons | Average Latency |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **1,000** | Linear Search | 0.00 ms | 506.8 | 1,000 | 22.81 $\mu$s |
| | Binary Search (Rec) | 0.16 ms | 8.8 | 10 | 1.75 $\mu$s |
| | Hash Table (Chained) | 1.20 ms | 1.4 | 2 | 0.38 $\mu$s |
| **10,000** | Linear Search | 0.00 ms | 4,699.1 | 10,000 | 407.24 $\mu$s |
| | Binary Search (Rec) | 1.93 ms | 12.3 | 13 | 2.41 $\mu$s |
| | Hash Table (Chained) | 5.84 ms | 1.4 | 0 | 0.38 $\mu$s |
| **100,000** | Linear Search | 0.00 ms | 48,100.7 | 100,000 | 7,931.51 $\mu$s |
| | Binary Search (Rec) | 55.01 ms | 15.7 | 16 | 3.20 $\mu$s |
| | Hash Table (Chained) | 143.37 ms | 1.3 | 0 | 0.38 $\mu$s |
| **1,000,000** | Linear Search | 0.00 ms | 475,849.0 | 1,000,000 | 86,497.02 $\mu$s |
| | Binary Search (Rec) | 807.81 ms | 19.1 | 20 | 5.84 $\mu$s |
| | Hash Table (Chained) | 2,324.25 ms | 1.4 | 2 | 0.40 $\mu$s |

### Task 12 Day-4 Challenge (50,000 Queries on 1,000,000 Records)
- **Chained Hash Table:** **0.079 seconds** ($635,630$ queries/sec, $1.26 \mu\text{s}$ mean latency).
- **Recursive Binary Search:** **0.374 seconds** ($133,816$ queries/sec, $7.16 \mu\text{s}$ mean latency).
- **Linear Search:** **5,079.94 seconds / 84.67 minutes** ($9.8$ queries/sec) $\to$ **Catastrophic Failure**.

---

## Submission Checklist Compliance
- [x] All 12 tasks documented in complete academic rigor.
- [x] Student Reg No (`192472347`) and Name (`Somashekar Naidu`) printed on all logs and graphs.
- [x] Seed configured to last 4 digits (`2347`).
- [x] All four dataset sizes evaluated ($1\text{K} \to 1\text{M}$).
- [x] Task 12 Day-4 challenge benchmarked and defended.
- [x] PDF report generated and stored in `report/DAA_A1_192472347.pdf`.

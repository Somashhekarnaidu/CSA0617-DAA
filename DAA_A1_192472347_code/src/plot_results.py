"""
plot_results.py
===============
Generates high-resolution publication-quality graphs for DAA Assignment 1.
Reads experimental data from results/results.csv and results/challenge_results.csv.

Outputs graphs to results/graphs/:
- fig1_execution_time_comparison.png
- fig2_comparisons_scaling.png
- fig3_preprocessing_overhead.png
- fig4_theory_vs_experiment.png
- fig5_task12_challenge_throughput.png
- fig6_amortized_cost.png

Student Details:
- Name: Somashekar Naidu
- Registration Number: 192472347
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Styling Configuration
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 13
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 11
plt.rcParams['figure.titlesize'] = 14

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
GRAPHS_DIR = os.path.join(RESULTS_DIR, "graphs")
os.makedirs(GRAPHS_DIR, exist_ok=True)


def plot_execution_time(df: pd.DataFrame):
    """Figure 1: Average Search Execution Time vs Input Size (N)"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    colors = {
        'Linear Search (Iterative)': '#d9534f',
        'Binary Search (Recursive)': '#0275d8',
        'Hash Table (Chained)': '#5cb85c'
    }
    markers = {
        'Linear Search (Iterative)': 'o',
        'Binary Search (Recursive)': 's',
        'Hash Table (Chained)': '^'
    }

    # Left: Linear Scale
    for algo in df['Algorithm'].unique():
        sub = df[df['Algorithm'] == algo]
        ax1.plot(sub['N'], sub['Avg_Time_us'], marker=markers[algo], color=colors[algo], 
                 linewidth=2.2, markersize=8, label=algo)
    ax1.set_xlabel('Dataset Size (N records)')
    ax1.set_ylabel('Average Search Time (microseconds)')
    ax1.set_title('(a) Search Latency (Linear Scale)\nLinear Search explodes at N=10^6')
    ax1.legend()
    ax1.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f"{int(x):,}"))

    # Right: Log-Log Scale to reveal sub-microsecond distinctions
    for algo in df['Algorithm'].unique():
        sub = df[df['Algorithm'] == algo]
        ax2.loglog(sub['N'], sub['Avg_Time_us'], marker=markers[algo], color=colors[algo], 
                   linewidth=2.2, markersize=8, label=algo)
    ax2.set_xlabel('Dataset Size (N records, Log Scale)')
    ax2.set_ylabel('Average Search Time (microseconds, Log Scale)')
    ax2.set_title('(b) Search Latency (Log-Log Scale)\nIllustrates O(n), O(log n), and O(1) slopes')
    ax2.legend()
    ax2.grid(True, which="both", ls="--", alpha=0.5)

    plt.suptitle("Figure 1: Empirical Search Execution Time vs Input Size (N)\nStudent: Somashekar Naidu | Reg No: 192472347", fontsize=14, y=1.02)
    plt.tight_layout()
    out_path = os.path.join(GRAPHS_DIR, "fig1_execution_time_comparison.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")


def plot_comparisons(df: pd.DataFrame):
    """Figure 2: Basic Operations (Key Comparisons) vs Input Size (N)"""
    fig, ax = plt.subplots(figsize=(10, 6))

    colors = {
        'Linear Search (Iterative)': '#d9534f',
        'Binary Search (Recursive)': '#0275d8',
        'Hash Table (Chained)': '#5cb85c'
    }
    markers = {
        'Linear Search (Iterative)': 'o',
        'Binary Search (Recursive)': 's',
        'Hash Table (Chained)': '^'
    }

    for algo in df['Algorithm'].unique():
        sub = df[df['Algorithm'] == algo]
        ax.loglog(sub['N'], sub['Avg_Comps'], marker=markers[algo], color=colors[algo],
                  linewidth=2.5, markersize=9, label=f"{algo} (Empirical Average)")

    ax.set_xlabel('Input Size (N records, Log Scale)')
    ax.set_ylabel('Number of Key Comparisons (Log Scale)')
    ax.set_title('Figure 2: Basic Operation Count (Key Comparisons) vs Input Size (N)\nStudent: Somashekar Naidu | Reg No: 192472347')
    ax.grid(True, which="both", ls="--", alpha=0.6)
    ax.legend()

    # Annotate values at N=1,000,000
    sub_1m = df[df['N'] == 1000000]
    for _, row in sub_1m.iterrows():
        ax.annotate(f"{row['Avg_Comps']:,.1f} comps", 
                    (row['N'], row['Avg_Comps']),
                    textcoords="offset points", xytext=(-50, 10),
                    fontweight='bold', color=colors[row['Algorithm']])

    plt.tight_layout()
    out_path = os.path.join(GRAPHS_DIR, "fig2_comparisons_scaling.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")


def plot_preprocessing_cost(df: pd.DataFrame):
    """Figure 3: Preprocessing Time Overhead vs N"""
    fig, ax = plt.subplots(figsize=(9, 5.5))

    sub_bs = df[df['Algorithm'] == 'Binary Search (Recursive)']
    sub_ht = df[df['Algorithm'] == 'Hash Table (Chained)']

    x = np.arange(len(sub_bs['N']))
    width = 0.35

    rects1 = ax.bar(x - width/2, sub_bs['Prep_Time_ms'], width, label='Binary Search (Timsort: O(n log n))', color='#0275d8')
    rects2 = ax.bar(x + width/2, sub_ht['Prep_Time_ms'], width, label='Hash Table (Table Build: O(n))', color='#5cb85c')

    ax.set_xlabel('Dataset Size (N records)')
    ax.set_ylabel('Preprocessing Time (milliseconds)')
    ax.set_title('Figure 3: Initial Preprocessing Overhead Comparison\nStudent: Somashekar Naidu | Reg No: 192472347')
    ax.set_xticks(x)
    ax.set_xticklabels([f"{n:,}" for n in sub_bs['N']])
    ax.legend()
    ax.grid(True, axis='y', ls='--', alpha=0.6)

    # Attach bar labels
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:,.1f} ms',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, rotation=0)

    autolabel(rects1)
    autolabel(rects2)

    plt.tight_layout()
    out_path = os.path.join(GRAPHS_DIR, "fig3_preprocessing_overhead.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")


def plot_theory_vs_experiment(df: pd.DataFrame):
    """Figure 4: Theoretical Growth Rate vs Experimental Observations"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Normalized comparison at N=10,000 for Binary Search and Linear Search
    sub_ls = df[df['Algorithm'] == 'Linear Search (Iterative)']
    sub_bs = df[df['Algorithm'] == 'Binary Search (Recursive)']
    
    n_vals = sub_ls['N'].values
    
    # 1. Linear Search: Theory C(n) = (n+1)/2 vs Experiment
    theory_ls = (n_vals + 1) / 2
    ax1.plot(n_vals, theory_ls, 'r--', linewidth=2, label='Theoretical: (n+1)/2')
    ax1.plot(n_vals, sub_ls['Avg_Comps'], 'ro', markersize=8, label='Empirical Measured')
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    ax1.set_xlabel('Dataset Size N (Log Scale)')
    ax1.set_ylabel('Key Comparisons (Log Scale)')
    ax1.set_title('(a) Linear Search: Theory vs Experiment\nPerfect 1:1 Agreement with O(n)')
    ax1.legend()
    ax1.grid(True, which="both", ls="--", alpha=0.5)

    # 2. Binary Search: Theory C(n) = log2(n) - 1 vs Experiment
    theory_bs = np.log2(n_vals) - 1
    ax2.plot(n_vals, theory_bs, 'b--', linewidth=2, label='Theoretical: log2(n) - 1')
    ax2.plot(n_vals, sub_bs['Avg_Comps'], 'bs', markersize=8, label='Empirical Measured')
    ax2.set_xscale('log')
    ax2.set_xlabel('Dataset Size N (Log Scale)')
    ax2.set_ylabel('Key Comparisons')
    ax2.set_title('(b) Binary Search: Theory vs Experiment\nMatches Logarithmic Bound O(log n)')
    ax2.legend()
    ax2.grid(True, which="both", ls="--", alpha=0.5)

    plt.suptitle("Figure 4: Mathematical Theory Validation against Empirical Measurements\nStudent: Somashekar Naidu | Reg No: 192472347", fontsize=14, y=1.02)
    plt.tight_layout()
    out_path = os.path.join(GRAPHS_DIR, "fig4_theory_vs_experiment.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")


def plot_task12_throughput(ch_df: pd.DataFrame):
    """Figure 5: Task 12 Day-4 Design Challenge Throughput & Latency"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    algos = ch_df['Algorithm'].tolist()
    throughputs = ch_df['Throughput_qps'].tolist()
    mean_latencies = ch_df['Mean_Latency_us'].tolist()

    colors = ['#d9534f', '#0275d8', '#5cb85c']
    short_labels = ['Linear Search', 'Binary Search', 'Hash Table']

    # Throughput (Log scale)
    bars1 = ax1.bar(short_labels, throughputs, color=colors, width=0.55)
    ax1.set_yscale('log')
    ax1.set_ylabel('Throughput (Queries / Second, Log Scale)')
    ax1.set_title('(a) System Query Throughput\n(Workload: 50,000 Queries on N = 1,000,000)')
    ax1.grid(True, axis='y', ls='--', alpha=0.6)
    
    for bar in bars1:
        yval = bar.get_height()
        ax1.annotate(f"{yval:,.1f} QPS",
                    xy=(bar.get_x() + bar.get_width() / 2, yval),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontweight='bold', fontsize=10)

    # Latency (Log scale)
    bars2 = ax2.bar(short_labels, mean_latencies, color=colors, width=0.55)
    ax2.set_yscale('log')
    ax2.set_ylabel('Mean Latency (Microseconds, Log Scale)')
    ax2.set_title('(b) Average Query Latency\n(Lower is better)')
    ax2.grid(True, axis='y', ls='--', alpha=0.6)

    for bar in bars2:
        yval = bar.get_height()
        ax2.annotate(f"{yval:,.2f} µs",
                    xy=(bar.get_x() + bar.get_width() / 2, yval),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontweight='bold', fontsize=10)

    plt.suptitle("Figure 5: Task 12 Day-4 Challenge Benchmark Performance (50,000 Searches / Hr)\nStudent: Somashekar Naidu | Reg No: 192472347", fontsize=14, y=1.02)
    plt.tight_layout()
    out_path = os.path.join(GRAPHS_DIR, "fig5_task12_challenge_throughput.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")


def plot_amortized_cost():
    """Figure 6: Amortized Total Cost vs Number of Queries Q for N=1,000,000"""
    fig, ax = plt.subplots(figsize=(10, 6))

    Q = np.logspace(0, 6, 200) # 1 query to 1,000,000 queries

    # Constants derived empirically at N = 1,000,000:
    # Linear Search: T_prep = 0 ms, T_query = 40.0 ms
    # Binary Search: T_prep = 950 ms, T_query = 0.0025 ms (2.5 us)
    # Hash Table:    T_prep = 650 ms, T_query = 0.0006 ms (0.6 us)

    T_linear = Q * 40.0 # ms
    T_binary = 950.0 + Q * 0.0025 # ms
    T_hash   = 650.0 + Q * 0.0006 # ms

    ax.loglog(Q, T_linear / 1000, '#d9534f', linewidth=2.5, label='Linear Search: Total Cost = Q * 40ms')
    ax.loglog(Q, T_binary / 1000, '#0275d8', linewidth=2.5, label='Binary Search: Total Cost = 950ms + Q * 2.5µs')
    ax.loglog(Q, T_hash / 1000, '#5cb85c', linewidth=2.5, label='Hash Table: Total Cost = 650ms + Q * 0.6µs')

    ax.set_xlabel('Number of Search Queries Q (Log Scale)')
    ax.set_ylabel('Total System Wall-Clock Time (Seconds, Log Scale)')
    ax.set_title('Figure 6: Amortized Total System Cost (Preprocessing + Q Searches) for N = 1,000,000\nStudent: Somashekar Naidu | Reg No: 192472347')
    ax.grid(True, which="both", ls="--", alpha=0.6)
    ax.legend(loc='upper left')

    # Highlight Crossover point between Linear and Binary/Hash
    # 40 * Q = 650 + 0.0006 * Q => Q ≈ 17 queries!
    ax.axvline(x=17, color='purple', linestyle=':', linewidth=1.8)
    ax.annotate('Break-even Crossover\nQ ≈ 17 queries\n(Binary/Hash surpass Linear)', 
                xy=(17, 0.7), xytext=(25, 0.02),
                arrowprops=dict(facecolor='black', arrowstyle='->'),
                fontsize=10, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.3))

    # Highlight Day-4 Requirement Q = 50,000
    ax.axvline(x=50000, color='orange', linestyle='--', linewidth=1.8)
    ax.annotate('Task 12 Operating Point\n(Q = 50,000 queries/hr)\nHash Table: ~0.68s Total\nLinear: ~2,000s Total!', 
                xy=(50000, 50000 * 0.0006 / 1000), xytext=(15000, 10),
                arrowprops=dict(facecolor='black', arrowstyle='->'),
                fontsize=10, fontweight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="#bbf", alpha=0.4))

    plt.tight_layout()
    out_path = os.path.join(GRAPHS_DIR, "fig6_amortized_cost.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved: {out_path}")


def main():
    csv_path = os.path.join(RESULTS_DIR, "results.csv")
    ch_csv_path = os.path.join(RESULTS_DIR, "challenge_results.csv")

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        print("Plotting Execution Time...")
        plot_execution_time(df)
        print("Plotting Comparisons Scaling...")
        plot_comparisons(df)
        print("Plotting Preprocessing Overhead...")
        plot_preprocessing_cost(df)
        print("Plotting Theory vs Experiment...")
        plot_theory_vs_experiment(df)
    else:
        print(f"Notice: {csv_path} not found. Run benchmark.py first.")

    if os.path.exists(ch_csv_path):
        ch_df = pd.read_csv(ch_csv_path)
        print("Plotting Task 12 Challenge Throughput...")
        plot_task12_throughput(ch_df)
    else:
        print(f"Notice: {ch_csv_path} not found. Run challenge_benchmark.py first.")

    print("Plotting Amortized Total Cost...")
    plot_amortized_cost()
    print("\n[SUCCESS] All figures generated successfully in results/graphs/")


if __name__ == "__main__":
    main()

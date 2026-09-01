"""
Plotting Script for Multi-Tier Benchmark Evaluation
Generates visual comparison charts strictly comparing Baseline vs FaaSLight Static:
1. results/latency_comparison.png (Cold Import & Total Latency: Baseline vs FaaSLight Static)
2. results/faaslight_vs_baseline_reduction.png (Code Loading & Total Latency % Reductions vs Paper Targets)
3. results/hitrate_and_memory.png (Memory RSS Footprint: Baseline vs FaaSLight Static)
"""

import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np


def main():
    res_dir = Path(__file__).parent.parent / "results"
    data_file = res_dir / "benchmark_data.json"

    if not data_file.exists():
        print(f"Error: {data_file} not found. Run run_benchmark.py first.")
        return

    with open(data_file, "r") as f:
        data = json.load(f)

    workload_data = data.get("workloads", data)
    reductions = data.get("reductions", {})

    workloads = list(workload_data.keys())
    clean_labels = ["Tier 1 (Light)", "Tier 2 (Medium)", "Tier 3 (Heavy)", "Blended Fleet"]
    
    # Strictly Baseline vs FaaSLight Static
    eval_modes = ["Baseline (Eager)", "Static-Only (FaaSLight)"]
    mode_colors = ["#c0392b", "#2980b9"]  # Dark Red for Baseline, Royal Teal/Blue for FaaSLight
    
    x = np.arange(len(workloads))
    width = 0.35

    # -------------------------------------------------------------
    # Chart 1: Latency Comparison across Tiers (Baseline vs FaaSLight)
    # -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5.5))
    plt.subplots_adjust(wspace=0.25)

    # Subplot 1A: Cold-Start Import Latency
    for i, mode in enumerate(eval_modes):
        import_latencies = [workload_data[w][mode]["avg_import_latency_ms"] for w in workloads]
        rects = ax1.bar(
            x + (i - 0.5) * width + width / 2,
            import_latencies,
            width,
            label=mode,
            color=mode_colors[i],
            edgecolor="black",
            linewidth=0.8,
            alpha=0.9
        )
        for rect in rects:
            height = rect.get_height()
            ax1.annotate(
                f"{height:.2f}ms",
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8.5,
                fontweight="bold"
            )

    ax1.set_title("Cold-Start / Code-Loading Latency (ms)", fontsize=11.5, fontweight="bold", pad=10)
    ax1.set_ylabel("Cold Import Latency (ms)", fontsize=10)
    ax1.set_xticks(x)
    ax1.set_xticklabels(clean_labels, fontsize=9.5)
    ax1.legend(loc="upper left", framealpha=0.9)
    ax1.grid(axis="y", linestyle="--", alpha=0.3)
    ax1.set_ylim(0, max([workload_data[w]["Baseline (Eager)"]["avg_import_latency_ms"] for w in workloads]) * 1.18)

    # Subplot 1B: Total End-to-End Latency
    for i, mode in enumerate(eval_modes):
        total_latencies = [workload_data[w][mode]["avg_total_response_ms"] for w in workloads]
        rects = ax2.bar(
            x + (i - 0.5) * width + width / 2,
            total_latencies,
            width,
            label=mode,
            color=mode_colors[i],
            edgecolor="black",
            linewidth=0.8,
            alpha=0.9
        )
        for rect in rects:
            height = rect.get_height()
            ax2.annotate(
                f"{height:.2f}ms",
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8.5,
                fontweight="bold"
            )

    ax2.set_title("Total End-to-End Response Latency (ms)", fontsize=11.5, fontweight="bold", pad=10)
    ax2.set_ylabel("Total Response Latency (ms)", fontsize=10)
    ax2.set_xticks(x)
    ax2.set_xticklabels(clean_labels, fontsize=9.5)
    ax2.legend(loc="upper left", framealpha=0.9)
    ax2.grid(axis="y", linestyle="--", alpha=0.3)
    ax2.set_ylim(0, max([workload_data[w]["Baseline (Eager)"]["avg_total_response_ms"] for w in workloads]) * 1.18)

    plt.suptitle("Serverless Cold-Start Optimization Evaluation: Baseline (Eager) vs. FaaSLight Static", fontsize=13, fontweight="bold")
    latency_chart_path = res_dir / "latency_comparison.png"
    plt.savefig(latency_chart_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {latency_chart_path}")

    # -------------------------------------------------------------
    # Chart 2: Empirical Savings Bounds Spectrum vs Paper Target
    # -------------------------------------------------------------
    fig, (ax_red1, ax_red2) = plt.subplots(1, 2, figsize=(15, 5.5))
    plt.subplots_adjust(wspace=0.25)

    faas_import_reds = [reductions[w]["FaaSLight_vs_Baseline"]["import_reduction_pct"] for w in workloads]
    faas_total_reds = [reductions[w]["FaaSLight_vs_Baseline"]["total_reduction_pct"] for w in workloads]
    tier_bar_colors = ["#3498db", "#e67e22", "#9b59b6", "#27ae60"]

    # Subplot A: Code Loading Reduction %
    bars1 = ax_red1.bar(clean_labels, faas_import_reds, color=tier_bar_colors, edgecolor="black", width=0.45, alpha=0.9)
    ax_red1.axhline(28.8, color="#c0392b", linestyle="--", linewidth=2, label="Reported in Paper (28.8% Target)")
    for bar in bars1:
        h = bar.get_height()
        ax_red1.annotate(f"{h:.1f}%", xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, 4),
                         textcoords="offset points", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax_red1.set_title("Code-Loading Time Reduction vs Baseline (%)", fontsize=11.5, fontweight="bold")
    ax_red1.set_ylabel("Reduction (%)", fontsize=10)
    ax_red1.set_ylim(0, 100)
    ax_red1.legend(loc="upper left", framealpha=0.9)
    ax_red1.grid(axis="y", linestyle="--", alpha=0.3)

    # Subplot B: Total Response Latency Reduction %
    bars2 = ax_red2.bar(clean_labels, faas_total_reds, color=tier_bar_colors, edgecolor="black", width=0.45, alpha=0.9)
    ax_red2.axhline(19.2, color="#c0392b", linestyle="--", linewidth=2, label="Reported in Paper (19.2% Target)")
    for bar in bars2:
        h = bar.get_height()
        va_pos = "bottom" if h >= 0 else "top"
        y_off = 4 if h >= 0 else -12
        ax_red2.annotate(f"{h:.1f}%", xy=(bar.get_x() + bar.get_width() / 2, h), xytext=(0, y_off),
                         textcoords="offset points", ha="center", va=va_pos, fontsize=9, fontweight="bold")
    ax_red2.set_title("Total Latency Reduction vs Baseline (%)", fontsize=11.5, fontweight="bold")
    ax_red2.set_ylabel("Reduction (%)", fontsize=10)
    ax_red2.set_ylim(-10, 55)
    ax_red2.legend(loc="upper right", framealpha=0.9)
    ax_red2.grid(axis="y", linestyle="--", alpha=0.3)

    plt.suptitle("Observed Savings Spectrum (FaaSLight vs Baseline) Compared to Paper Targets", fontsize=13, fontweight="bold")
    spectrum_chart_path = res_dir / "faaslight_vs_baseline_reduction.png"
    plt.savefig(spectrum_chart_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {spectrum_chart_path}")

    # -------------------------------------------------------------
    # Chart 3: Runtime Memory Footprint (Baseline vs FaaSLight Static)
    # -------------------------------------------------------------
    fig, ax3 = plt.subplots(1, 1, figsize=(10, 5))

    for i, mode in enumerate(eval_modes):
        mem_vals = [workload_data[w][mode]["avg_memory_rss_mb"] for w in workloads]
        rects = ax3.bar(
            x + (i - 0.5) * width + width / 2,
            mem_vals,
            width,
            label=mode,
            color=mode_colors[i],
            edgecolor="black",
            linewidth=0.8,
            alpha=0.85
        )
        for rect in rects:
            height = rect.get_height()
            ax3.annotate(
                f"{height:.1f}MB",
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8.5,
                fontweight="bold"
            )

    ax3.set_title("Runtime Memory Footprint (RSS MB): Baseline vs. FaaSLight Static", fontsize=12, fontweight="bold", pad=10)
    ax3.set_ylabel("Memory (MB)", fontsize=10)
    ax3.set_xticks(x)
    ax3.set_xticklabels(clean_labels, fontsize=9.5)
    ax3.set_ylim(0, 30)
    ax3.legend(loc="lower right", framealpha=0.9)
    ax3.grid(axis="y", linestyle="--", alpha=0.3)

    tradeoff_chart_path = res_dir / "hitrate_and_memory.png"
    plt.savefig(tradeoff_chart_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {tradeoff_chart_path}")


if __name__ == "__main__":
    main()




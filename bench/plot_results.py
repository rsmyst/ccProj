"""Render compact, report-ready benchmark figures from benchmark_data.json."""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


PALETTE = {
    "Baseline (Eager)": "#6B7280",
    "V1 (Static / FaaSLight)": "#F97316",
    "V2 (Predictive Preload)": "#22C55E",
}


def load_data() -> tuple[Path, dict]:
    result_dir = Path(__file__).parent.parent / "results"
    with (result_dir / "benchmark_data.json").open(encoding="utf-8") as handle:
        return result_dir, json.load(handle)


def style_axes(ax: plt.Axes) -> None:
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#CFD8DC", linewidth=0.8, alpha=0.65)
    ax.set_axisbelow(True)


def save_latency_chart(result_dir: Path, workloads: list[str], data: dict) -> None:
    labels = ["Tier 1", "Tier 2", "Tier 3", "Fleet"]
    x = np.arange(len(workloads))
    modes = ["Baseline (Eager)", "V1 (Static / FaaSLight)", "V2 (Predictive Preload)"]
    width = 0.24
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.7), constrained_layout=True)
    for axis, metric, title, ylabel in [
        (axes[0], "avg_import_latency_ms", "Code loading", "ms"),
        (axes[1], "avg_total_response_ms", "End-to-end response", "ms"),
    ]:
        for index, mode in enumerate(modes):
            values = [data["workloads"][workload][mode][metric] for workload in workloads]
            labels_by_mode = ["Baseline", "V1 (FaaSLight)", "PCSO"]
            axis.bar(x + (index - 1) * width, values, width,
                     label=labels_by_mode[index],
                     color=PALETTE[mode])
        axis.set_title(title, loc="left", fontweight="bold")
        axis.set_ylabel(ylabel)
        axis.set_xticks(x, labels)
        style_axes(axis)
    axes[1].legend(frameon=False, fontsize=8, loc="upper right")
    fig.suptitle("Baseline vs V1 vs PCSO latency comparison", x=0.02, ha="left", fontweight="bold")
    fig.savefig(result_dir / "latency_comparison.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def save_reduction_chart(result_dir: Path, workloads: list[str], data: dict) -> None:
    labels = ["Tier 1", "Tier 2", "Tier 3", "Fleet"]
    x = np.arange(len(workloads))
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.7), constrained_layout=True)
    for axis, metric, title in [
        (axes[0], "import_reduction_pct", "Code-loading reduction"),
        (axes[1], "total_reduction_pct", "Total latency reduction"),
    ]:
        v1 = [data["reductions"][workload]["V1_vs_Baseline"][metric] for workload in workloads]
        pcso = [data["reductions"][workload]["V2_vs_Baseline"][metric] for workload in workloads]
        axis.bar(x - 0.18, v1, 0.36, label="V1 (FaaSLight)", color=PALETTE["V1 (Static / FaaSLight)"])
        axis.bar(x + 0.18, pcso, 0.36, label="PCSO", color=PALETTE["V2 (Predictive Preload)"])
        axis.axhline(0, color="#455A64", linewidth=0.8)
        axis.set_title(title, loc="left", fontweight="bold")
        axis.set_ylabel("reduction (%)")
        axis.set_ylim(min(-5, min(v1 + pcso) - 5), 100)
        axis.set_xticks(x, labels)
        style_axes(axis)
    axes[1].legend(frameon=False, fontsize=8, loc="upper right")
    fig.suptitle("PCSO improvement over the eager baseline", x=0.02, ha="left", fontweight="bold")
    fig.savefig(result_dir / "faaslight_vs_baseline_reduction.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def save_tradeoff_chart(result_dir: Path, workloads: list[str], data: dict) -> None:
    labels = ["Tier 1", "Tier 2", "Tier 3", "Fleet"]
    x = np.arange(len(workloads))
    fig, axis = plt.subplots(figsize=(10, 4.6), constrained_layout=True)
    for mode in ["Baseline (Eager)", "V1 (Static / FaaSLight)", "V2 (Predictive Preload)"]:
        values = [data["workloads"][workload][mode]["avg_memory_rss_mb"] for workload in workloads]
        label = {"Baseline (Eager)": "Baseline", "V1 (Static / FaaSLight)": "V1 (FaaSLight)", "V2 (Predictive Preload)": "PCSO"}[mode]
        axis.plot(x, values, marker="o", linewidth=2.2,
                  label=label,
                  color=PALETTE[mode])
    axis.set_title("Memory overhead stays bounded", loc="left", fontweight="bold")
    axis.set_ylabel("average RSS (MB)")
    axis.set_xticks(x, labels)
    style_axes(axis)
    axis.legend(frameon=False, fontsize=8, ncol=3, loc="lower right")
    fig.savefig(result_dir / "hitrate_and_memory.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    result_dir, data = load_data()
    workloads = list(data["workloads"])
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10})
    save_latency_chart(result_dir, workloads, data)
    save_reduction_chart(result_dir, workloads, data)
    save_tradeoff_chart(result_dir, workloads, data)
    print(f"Rendered benchmark figures in {result_dir}")


if __name__ == "__main__":
    main()

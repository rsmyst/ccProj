#!/usr/bin/env python3
"""
Predictive Serverless Cold-Start Optimizer — CLI Entrypoint

Static dependency analyzer, predictive runtime, and benchmark suite
Usage:
    python main.py --file src/workloads/core_api.py
    python main.py --dir src/workloads/
    python main.py --dir src/workloads/ --graph
    python main.py --dir src/workloads/ --json
"""

import argparse
import json
import sys
from pathlib import Path

from src.analyzer import StaticDependencyAnalyzer


def parse_args():
    parser = argparse.ArgumentParser(
        description="Predictive Serverless Cold-Start Optimizer"
    )

    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "-f", "--file",
        type=str,
        help="Path to a single Python file to analyze"
    )
    group.add_argument(
        "-d", "--dir",
        type=str,
        default="src/workloads",
        help="Path to a directory of Python files to analyze (default: src/workloads)"
    )

    parser.add_argument(
        "-g", "--graph",
        action="store_true",
        help="Generate and print ASCII dependency call graph"
    )
    parser.add_argument(
        "-j", "--json",
        action="store_true",
        help="Output raw analysis results as formatted JSON"
    )
    parser.add_argument(
        "--predict",
        action="store_true",
        help="Run a transition predictor demonstration"
    )
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Run the reproducible Baseline/V1/V2 benchmark"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    # Run Objective 2: Transition Predictor Demo
    if args.predict:
        from src.predictor import TransitionPredictor
        predictor = TransitionPredictor()
        sample_transitions = [
            ("core_api", "payment_gateway"),
            ("core_api", "payment_gateway"),
            ("core_api", "payment_gateway"),
            ("core_api", "feature_recommendation"),
            ("payment_gateway", "notification_service"),
            ("payment_gateway", "notification_service"),
            ("payment_gateway", "analytics_pipeline"),
            ("notification_service", "analytics_pipeline")
        ]
        print("=" * 70)
        print("  RUNTIME TRANSITION PREDICTOR (Markov Sequence Engine)")
        print("=" * 70)
        print(f"Training on sample sequence of {len(sample_transitions)} transitions...")
        for src, dst in sample_transitions:
            hit = predictor.evaluate_and_record(src, dst)
            print(f"  Transition: {src:<22} -> {dst:<22} (Predicted correctly: {hit})")
        print("-" * 70)
        print(f"Overall Predictor Accuracy: {predictor.accuracy:.1f}%")
        print("\nNext-hop Predictions (Top-1):")
        for src in ["core_api", "payment_gateway", "notification_service"]:
            preds = predictor.predict_next(src, top_k=2)
            pred_str = ", ".join([f"{t} (P={p*100:.1f}%)" for t, p in preds])
            print(f"  From [{src}]: -> {pred_str}")
        print("=" * 70)
        sys.exit(0)

    # Run Objective 3: Benchmark Suite
    if args.benchmark:
        from bench.run_benchmark import main as run_bench_main
        run_bench_main()
        sys.exit(0)

    # Run Objective 1: Static Dependency Analyzer
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Error: Target file does not exist: {file_path}")
            sys.exit(1)

        report = StaticDependencyAnalyzer.analyze_file(file_path)
        if args.json:
            print(json.dumps(report.to_dict(), indent=2))
        else:
            report.print_summary()

    else:
        dir_path = Path(args.dir)
        if not dir_path.exists() or not dir_path.is_dir():
            print(f"Error: Target directory does not exist: {dir_path}")
            sys.exit(1)

        reports = StaticDependencyAnalyzer.analyze_directory(dir_path)

        if args.json:
            data = {k: v.to_dict() for k, v in reports.items()}
            print(json.dumps(data, indent=2))
        elif args.graph:
            print(StaticDependencyAnalyzer.generate_ascii_graph(reports))
        else:
            print("=" * 70)
            print(f"  STATIC DEPENDENCY ANALYSIS SUMMARY (Directory: {dir_path})")
            print("=" * 70)
            print(f"{'Module':<28} | {'Total':<6} | {'Indispensable (Eager)':<24} | {'Optional (Lazy)'}")
            print("-" * 70)
            for mod, rep in reports.items():
                ind_str = ", ".join(rep.indispensable_imports) or "(none)"
                opt_str = ", ".join(rep.optional_imports) or "(none)"
                print(f"{mod:<28} | {rep.total_imports:<6} | {ind_str:<24} | {opt_str}")
            print("=" * 70)
            print("Tip: Run with --file <path> for detailed line-by-line inspection, or --graph for dependency trees.\n")


if __name__ == "__main__":
    main()

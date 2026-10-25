# Predictive Serverless Cold-Start Optimizer

This project measures three versions of a Python serverless runtime:

- **Baseline**: eagerly imports the full static dependency set.
- **V1**: uses AST analysis to import only indispensable dependencies at startup.
- **V2**: adds online Markov next-hop prediction and preloads the predicted module closure.

The benchmark uses light, medium, heavy, and blended workloads from `src/workloads`. The latest reproducible run is stored in [`results/benchmark_data.json`](results/benchmark_data.json), with figures in [`results/`](results/).

## Run

```bash
python main.py --dir src/workloads
python main.py --dir src/workloads --graph
python main.py --predict
python main.py --benchmark
python bench/plot_results.py
python -m pytest -q
```

The benchmark uses fixed seeds, 24 invocations per tier, 32 blended invocations, and reports import latency, handler latency, total response latency, p95, memory, and predictive cache hits. Background preload time is recorded separately from request latency.

## Documents

- [`report.pdf`](report.pdf) — compiled technical report
- [`presentation.pdf`](presentation.pdf) — compiled presentation
- [`report.tex`](report.tex) and [`presentation.tex`](presentation.tex) — source files
- [`diagrams/`](diagrams/) — Mermaid source and rendered runtime diagrams

Compile the documents with:

```bash
tectonic report.tex
tectonic presentation.tex
```

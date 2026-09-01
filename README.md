# Predictive Serverless Cold-Start Optimizer

> **Milestone 1: Static Dependency Analyzer (Objective 1)**  
> An AST-based dependency analyzer for serverless functions inspired by **FaaSLight**.

---

## 🎯 Project Roadmap & Status

| Milestone | Objective | Description | Status |
| :--- | :--- | :--- | :---: |
| **Milestone 1** | **Objective 1: Static Dependency Analyzer** | AST-based code analysis classifying dependencies into indispensable (eager) vs. optional (deferred/lazy). | **COMPLETED & RUNNABLE** |
| **Milestone 2** | **Objective 2: Runtime Transition Predictor** | Frequency-based Markov matrix predicting subsequent function transitions ($A \to B \to C$). | *Not Implemented* |
| **Milestone 3** | **Objective 3: Preloader & Benchmark Harness** | Module preloader and cold-start benchmark comparing baseline vs. static vs. predictive preloading. | *Not Implemented* |

---

## 🚀 How to Run Milestone 1

### 1. Analyze a Directory of Functions
Scan all serverless functions in a directory (defaults to `src/workloads`):
```bash
python main.py --dir src/workloads
```

### 2. View the Dependency Call Graph
Generate an ASCII dependency tree showing indispensable vs. optional dependencies:
```bash
python main.py --dir src/workloads --graph
```

### 3. Detailed File Inspection
Analyze an individual function file line-by-line:
```bash
python main.py --file src/workloads/core_api.py
python main.py --file src/workloads/feature_recommendation.py
```

### 4. Export JSON Output
```bash
python main.py --file src/workloads/core_api.py --json
python main.py --dir src/workloads --json
```

### 5. Check Unimplemented Modules
```bash
python main.py --predict
python main.py --benchmark
```

### 6. Run Unit Tests
```bash
python -m pytest tests/test_analyzer.py -v
```

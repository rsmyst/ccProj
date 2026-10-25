"""
Objective 3: Module Preloader (Milestone 3)
Dynamically imports and manages prewarmed modules in memory (sys.modules)
to eliminate cold-start import latency during subsequent invocations.
"""

import importlib
import sys
import time
from typing import Iterable, Set


class ModulePreloader:
    """
    Manages in-memory preloading and eviction of Python modules.
    """

    def __init__(self):
        self.preloaded_modules: Set[str] = set()

    def preload(self, modules: Iterable[str]) -> float:
        """
        Preloads the specified list of module paths into sys.modules.
        Returns total preload time in milliseconds.
        """
        t_start = time.perf_counter()
        for mod in modules:
            if not mod:
                continue
            try:
                # If module is already in sys.modules, reload/import ensures reference
                if mod not in sys.modules:
                    importlib.import_module(mod)
                self.preloaded_modules.add(mod)
            except Exception as e:
                # In simulation or missing modules, continue gracefully
                pass

        elapsed_ms = (time.perf_counter() - t_start) * 1000.0
        return elapsed_ms

    def evict(self, modules: Iterable[str]) -> None:
        """Evicts specified modules from sys.modules and internal cache."""
        for mod in modules:
            if mod in sys.modules:
                del sys.modules[mod]
            self.preloaded_modules.discard(mod)

    def evict_all_workloads(self, prefix: str = "src.workloads", preserve: Iterable[str] = ()) -> None:
        """Evict workload modules, optionally retaining a preloaded working set."""
        keep = set(preserve)
        to_evict = [m for m in sys.modules if m.startswith(prefix) and m not in keep]
        for m in to_evict:
            del sys.modules[m]
        self.preloaded_modules.intersection_update(keep)

    def is_preloaded(self, module: str) -> bool:
        """Checks if module is currently loaded in sys.modules."""
        return module in sys.modules

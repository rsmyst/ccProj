"""Lightweight in-memory KV cache helper."""
import time
time.sleep(0.0008)  # 0.8ms
_STORE = {}
def get(k): return _STORE.get(k)
def set(k, v): _STORE[k] = v

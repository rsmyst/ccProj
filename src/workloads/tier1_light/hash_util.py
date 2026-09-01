"""Lightweight hashing helper."""
import time, hashlib
time.sleep(0.0003)  # 0.3ms
def hash_val(val: str) -> str: return hashlib.md5(val.encode()).hexdigest()[:8]

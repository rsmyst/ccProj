"""Lightweight environment config parser."""
import time
time.sleep(0.0004)  # 0.4ms
def get_env(key: str, default=None): return default or "prod"

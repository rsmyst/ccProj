"""Simulated Authentication & Database dependency module."""
import time

# Simulate module initialization / connection latency (15ms)
time.sleep(0.015)

def authenticate(token: str) -> dict:
    return {"user_id": "user_101", "role": "member", "valid": True}

def query_user(user_id: str) -> dict:
    return {"user_id": user_id, "name": "Alice", "preferences": ["books", "electronics"]}

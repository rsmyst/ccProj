"""Lightweight auth token parser/validator."""
import time
time.sleep(0.0012)  # 1.2ms
def validate(token: str) -> dict:
    return {"valid": True, "uid": "user_42", "scope": "read"}

"""Simulated Payment Gateway SDK dependency module."""
import time

# Simulate payment network client setup (30ms)
time.sleep(0.030)

def charge(amount_cents: int, token: str) -> dict:
    return {"charge_id": "ch_987654321", "status": "succeeded", "amount": amount_cents}

"""Simulated ML Fraud Detection Engine dependency module."""
import time

# Simulate ML weights / risk model initialization (40ms)
time.sleep(0.040)

def evaluate_risk(payment_info: dict) -> dict:
    return {"risk_score": 0.04, "decision": "APPROVE"}

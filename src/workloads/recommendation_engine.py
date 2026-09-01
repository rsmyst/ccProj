"""Simulated Recommendation Engine / ML Model dependency module."""
import time

# Simulate heavy ML weights loading latency (45ms)
time.sleep(0.045)

def compute_recommendations(user_id: str) -> list[str]:
    return ["item_42", "item_88", "item_99"]

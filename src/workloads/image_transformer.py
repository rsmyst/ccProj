"""Simulated Image Processing / CV dependency module."""
import time

# Simulate image processing library initialization latency (35ms)
time.sleep(0.035)

def process_image(image_id: str) -> dict:
    return {"image_id": image_id, "format": "webp", "size_kb": 120, "compressed": True}

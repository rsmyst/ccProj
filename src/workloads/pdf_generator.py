"""Simulated PDF Document Rendering dependency module."""
import time

# Simulate PDF typography and canvas engine initialization (30ms)
time.sleep(0.030)

def generate_pdf(text: str) -> bytes:
    return b"%PDF-1.4 simulated pdf output"

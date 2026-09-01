"""Simulated Optical Character Recognition Engine dependency module."""
import time

# Simulate deep learning OCR model loading (50ms)
time.sleep(0.050)

def extract_text(doc_bytes: bytes) -> str:
    return "INVOICE #2026-889 Total: $1,420.00 Paid"

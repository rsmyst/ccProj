"""Simulated Object Storage (S3 / GCS) dependency module."""
import time

# Simulate cloud storage client connection (12ms)
time.sleep(0.012)

def get_object(bucket: str, key: str) -> bytes:
    return b"SAMPLE_DOCUMENT_BINARY_CONTENT"

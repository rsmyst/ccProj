"""Simulated Email Delivery / Template Engine dependency module."""
import time

# Simulate SMTP / SES client initialization (20ms)
time.sleep(0.020)

def send_email(recipient: str, subject: str, body: str) -> bool:
    return True

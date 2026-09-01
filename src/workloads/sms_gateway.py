"""Simulated Telecom / SMS Gateway dependency module."""
import time

# Simulate carrier protocol negotiation (20ms)
time.sleep(0.020)

def send_sms(phone: str, text: str) -> str:
    return "MSG_SENT_ID_7781"

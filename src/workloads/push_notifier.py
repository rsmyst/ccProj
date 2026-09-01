"""Simulated Mobile Push Notification (APNS/FCM) module."""
import time

# Simulate push service connection (15ms)
time.sleep(0.015)

def send_push(device_token: str, message: str) -> bool:
    return True

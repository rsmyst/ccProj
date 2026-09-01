"""Multi-channel Notification microservice endpoint."""
import time
import src.workloads.auth_db as auth_db

def handler(event: dict) -> dict:
    t_start = time.perf_counter()
    user_id = event.get("user_id", "user_101")
    user = auth_db.query_user(user_id)
    channel = event.get("channel", "email")
    delivered = False
    
    # Conditional optional channels
    if channel == "email":
        import src.workloads.email_sender as email_sender
        delivered = email_sender.send_email("user@example.com", "Order Update", "Your order has shipped")
    elif channel == "sms":
        import src.workloads.sms_gateway as sms_gateway
        delivered = bool(sms_gateway.send_sms("+1234567890", "Your order has shipped"))
    elif channel == "push":
        import src.workloads.push_notifier as push_notifier
        delivered = push_notifier.send_push("dev_tok_99", "Your order has shipped")
        
    time.sleep(0.004)  # Simulated 4ms compute
    return {
        "status": 200,
        "endpoint": "notification_service",
        "channel": channel,
        "delivered": delivered,
        "exec_time_ms": (time.perf_counter() - t_start) * 1000
    }

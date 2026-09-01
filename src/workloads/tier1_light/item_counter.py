"""Tier 1 Endpoint: Simple hit counter & telemetry."""
import time, json
import src.workloads.tier1_light.hash_util as hash_util
import src.workloads.tier1_light.cache_kv as cache_kv

def handler(event: dict) -> dict:
    t_start = time.perf_counter()
    key = hash_util.hash_val(event.get("item_id", "default_item"))
    val = (cache_kv.get(key) or 0) + 1
    cache_kv.set(key, val)
    
    if event.get("threshold_alert", False):
        import src.workloads.tier1_light.slack_alert as slack_alert
        slack_alert.send_alert(f"Item {key} reached {val}")
        
    time.sleep(0.001)  # 1ms execution
    return {"status": 200, "key": key, "count": val, "exec_time_ms": (time.perf_counter() - t_start) * 1000}

"""Tier 1 Endpoint: Health check & uptime."""
import time, json
import src.workloads.tier1_light.sys_metrics as sys_metrics

def handler(event: dict) -> dict:
    t_start = time.perf_counter()
    metrics = sys_metrics.get_load()
    
    # Optional debug logger
    if event.get("debug"):
        import src.workloads.tier1_light.debug_logger as debug_logger
        debug_logger.log_debug("Health check invoked")
        
    time.sleep(0.001)  # 1ms execution
    return {"status": "HEALTHY", "metrics": metrics, "exec_time_ms": (time.perf_counter() - t_start) * 1000}

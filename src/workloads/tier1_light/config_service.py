"""Tier 1 Endpoint: App Configuration & Feature Flags."""
import time, json
import src.workloads.tier1_light.env_parser as env_parser
import src.workloads.tier1_light.cache_kv as cache_kv

def handler(event: dict) -> dict:
    t_start = time.perf_counter()
    env = env_parser.get_env("STAGE", "prod")
    flags = {"env": env, "v2_enabled": True}
    
    if event.get("sync_remote", False):
        import src.workloads.tier1_light.remote_config_sync as remote_config_sync
        flags.update(remote_config_sync.fetch_overrides())
        
    time.sleep(0.0015)  # 1.5ms execution
    return {"status": 200, "flags": flags, "exec_time_ms": (time.perf_counter() - t_start) * 1000}

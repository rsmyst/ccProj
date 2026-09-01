"""Tier 1 Endpoint: Lightweight user profile fetcher."""
import time, json
import src.workloads.tier1_light.cache_kv as cache_kv
import src.workloads.tier1_light.auth_token_validator as auth_token_validator

def handler(event: dict) -> dict:
    t_start = time.perf_counter()
    auth = auth_token_validator.validate(event.get("token", "default"))
    cached = cache_kv.get(auth["uid"])
    
    avatar = None
    if event.get("include_avatar", False):
        import src.workloads.tier1_light.gravatar_resolver as gravatar_resolver
        avatar = gravatar_resolver.get_avatar("user@example.com")
        
    time.sleep(0.002)  # 2ms execution
    return {"status": 200, "user": auth["uid"], "avatar": avatar, "exec_time_ms": (time.perf_counter() - t_start) * 1000}

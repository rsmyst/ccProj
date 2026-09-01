"""Tier 3 Endpoint: Media transformation & metadata pipeline."""
import time
import src.workloads.tier3_heavy.auth_db as auth_db

def handler(event: dict) -> dict:
    t_start = time.perf_counter()
    _ = auth_db.authenticate(event.get("token"))
    
    res = None
    if event.get("transform", True):
        import src.workloads.tier3_heavy.cv_transformer as cv_transformer
        res = cv_transformer.transform_img(b"raw")
        
    meta = None
    if event.get("extract_meta", True):
        import src.workloads.tier3_heavy.metadata_extractor as metadata_extractor
        meta = metadata_extractor.extract_meta(b"raw")
        
    time.sleep(0.008)  # 8ms execution
    return {"status": 200, "result": res, "meta": meta, "exec_time_ms": (time.perf_counter() - t_start) * 1000}

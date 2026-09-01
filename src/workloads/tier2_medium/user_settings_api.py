"""Tier 2 Endpoint: User Preferences & Access Control."""
import time, json
import src.workloads.tier2_medium.jwt_verifier as jwt_verifier
import src.workloads.tier2_medium.rbac_engine as rbac_engine
import src.workloads.tier2_medium.db_orm as db_orm

def handler(event: dict) -> dict:
    t_start = time.perf_counter()
    claims = jwt_verifier.verify(event.get("token"))
    rbac_engine.check_permission(claims.get("role", "admin"), "write_settings")
    settings = db_orm.query("user_settings", claims["sub"])
    
    if event.get("notify_user", False):
        import src.workloads.tier2_medium.email_dispatcher as email_dispatcher
        email_dispatcher.dispatch_email("user@company.com", "settings_changed")
        
    if event.get("compliance_audit", False):
        import src.workloads.tier2_medium.audit_logger as audit_logger
        audit_logger.record_audit("update_settings", claims["sub"])
        
    time.sleep(0.006)  # 6ms execution
    return {"status": 200, "settings": settings, "exec_time_ms": (time.perf_counter() - t_start) * 1000}

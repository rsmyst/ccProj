"""Tier 2 Endpoint: Stock query & reservations."""
import time, json
import src.workloads.tier2_medium.auth_db as auth_db
import src.workloads.tier2_medium.cache_redis as cache_redis
import src.workloads.tier2_medium.db_orm as db_orm

def handler(event: dict) -> dict:
    t_start = time.perf_counter()
    _ = auth_db.authenticate(event.get("token"))
    sku = event.get("sku", "SKU_772")
    stock = db_orm.query("inventory", sku)
    
    if stock.get("qty", 10) < 5 and event.get("low_stock", False):
        import src.workloads.tier2_medium.restock_alert as restock_alert
        restock_alert.trigger_alert(sku)
        
    if event.get("sync_supplier", False):
        import src.workloads.tier2_medium.supplier_webhook as supplier_webhook
        supplier_webhook.notify_supplier(sku, 50)
        
    time.sleep(0.005)  # 5ms execution
    return {"status": 200, "sku": sku, "stock": 42, "exec_time_ms": (time.perf_counter() - t_start) * 1000}

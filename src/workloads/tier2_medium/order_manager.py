"""Tier 2 Endpoint: Order Placement & Checkout."""
import time, json
import src.workloads.tier2_medium.auth_db as auth_db
import src.workloads.tier2_medium.schema_validator as schema_validator
import src.workloads.tier2_medium.db_orm as db_orm

def handler(event: dict) -> dict:
    t_start = time.perf_counter()
    user = auth_db.authenticate(event.get("token"))
    schema_validator.validate_payload(event)
    db_orm.insert("orders", {"user": user["user_id"], "total": 150})
    
    invoice = None
    if event.get("send_invoice", False):
        import src.workloads.tier2_medium.invoice_emitter as invoice_emitter
        invoice = invoice_emitter.emit_invoice(event)
        
    discount = 0
    if event.get("coupon_code"):
        import src.workloads.tier2_medium.coupon_calculator as coupon_calculator
        discount = coupon_calculator.apply_discount(event.get("coupon_code"), 150)
        
    time.sleep(0.005)  # 5ms execution
    return {"status": 200, "order_id": "ord_881", "invoice": invoice, "exec_time_ms": (time.perf_counter() - t_start) * 1000}

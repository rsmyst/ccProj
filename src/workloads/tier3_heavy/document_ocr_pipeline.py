"""Tier 3 Endpoint: Document OCR Extraction & PDF Report."""
import time
import src.workloads.tier3_heavy.auth_db as auth_db
import src.workloads.tier3_heavy.storage_s3 as storage_s3

def handler(event: dict) -> dict:
    t_start = time.perf_counter()
    _ = auth_db.authenticate(event.get("token"))
    data = storage_s3.get_file("invoice.pdf")
    
    text = "raw"
    if event.get("ocr_scan", True):
        import src.workloads.tier3_heavy.tesseract_ocr as tesseract_ocr
        text = tesseract_ocr.parse_ocr(data)
        
    pdf = None
    if event.get("compile_pdf", True):
        import src.workloads.tier3_heavy.pdf_canvas as pdf_canvas
        pdf = pdf_canvas.render_pdf(text)
        
    time.sleep(0.010)  # 10ms execution
    return {"status": 200, "text": text, "pdf_len": len(pdf) if pdf else 0, "exec_time_ms": (time.perf_counter() - t_start) * 1000}

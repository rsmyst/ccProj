"""Document Processing & OCR microservice endpoint."""
import time
import src.workloads.auth_db as auth_db
import src.workloads.storage_s3 as storage_s3

def handler(event: dict) -> dict:
    t_start = time.perf_counter()
    user_id = event.get("user_id", "user_101")
    _ = auth_db.query_user(user_id)
    doc_bytes = storage_s3.get_object("company-docs", event.get("key", "invoice.pdf"))
    
    # Conditional / Optional heavy OCR engine
    text = "Plain text content"
    if event.get("perform_ocr", True):
        import src.workloads.ocr_engine as ocr_engine
        text = ocr_engine.extract_text(doc_bytes)
        
    # Optional PDF report generator
    import src.workloads.pdf_generator as pdf_generator
    summary_pdf = pdf_generator.generate_pdf(text)
    
    time.sleep(0.012)  # Simulated 12ms compute
    return {
        "status": 200,
        "endpoint": "document_processor",
        "extracted_text_len": len(text),
        "pdf_bytes_len": len(summary_pdf),
        "exec_time_ms": (time.perf_counter() - t_start) * 1000
    }

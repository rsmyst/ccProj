import pytest
from src.runtime import ServerlessRuntimeSimulator, ExecutionMode

def test_runtime_baseline_execution():
    runtime = ServerlessRuntimeSimulator(mode=ExecutionMode.BASELINE)
    metrics = runtime.invoke("core_api", event={"token": "test_token"})
    assert metrics.endpoint == "core_api"
    assert metrics.cold_start is True
    assert metrics.total_response_ms > 0
    assert metrics.import_latency_ms > 0

def test_runtime_static_only_execution():
    runtime = ServerlessRuntimeSimulator(mode=ExecutionMode.STATIC_ONLY)
    metrics = runtime.invoke("payment_gateway", event={"amount": 50})
    assert metrics.endpoint == "payment_gateway"
    assert metrics.cold_start is True
    assert metrics.total_response_ms > 0
    assert metrics.cache_hit is False

def test_runtime_predictive_execution():
    runtime = ServerlessRuntimeSimulator(mode=ExecutionMode.STATIC_PREDICTIVE)
    # 1. Warm up transition history: core_api -> feature_recommendation
    runtime.invoke("core_api")
    runtime.invoke("feature_recommendation")
    
    # 2. Invoke sequence again: core_api -> feature_recommendation (should hit predictor)
    runtime.invoke("core_api")
    m = runtime.invoke("feature_recommendation")
    assert m.cache_hit is True
    assert m.import_latency_ms < 1.0

def test_runtime_expanded_endpoints():
    runtime = ServerlessRuntimeSimulator(mode=ExecutionMode.STATIC_ONLY)
    endpoints = ["document_processor", "notification_service", "analytics_pipeline", "payment_gateway"]
    for ep in endpoints:
        m = runtime.invoke(ep)
        assert m.endpoint == ep
        assert m.total_response_ms > 0


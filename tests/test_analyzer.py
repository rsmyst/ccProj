import pytest
import tempfile
import pathlib
from src.analyzer import StaticDependencyAnalyzer

def test_ast_analyzer_classification():
    code = """
import os
import sys
from collections import defaultdict

def handler(event):
    if event.get("debug"):
        import logging
    import json
    return "ok"
"""
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(code)
        f.flush()
        temp_path = f.name

    try:
        report = StaticDependencyAnalyzer.analyze_file(temp_path, "sample_service")
        assert "os" in report.indispensable_imports
        assert "sys" in report.indispensable_imports
        assert "collections" in report.indispensable_imports
        assert "logging" in report.optional_imports
        assert "json" in report.optional_imports
        assert report.total_imports == 5
        assert report.module_name == "sample_service"
    finally:
        pathlib.Path(temp_path).unlink(missing_ok=True)

def test_workload_analyzer():
    core_report = StaticDependencyAnalyzer.analyze_file("src/workloads/core_api.py")
    assert "src.workloads.auth_db" in core_report.indispensable_imports
    assert "src.workloads.noise_reporting" in core_report.optional_imports

def test_directory_analysis_and_graph():
    reports = StaticDependencyAnalyzer.analyze_directory("src/workloads")
    assert "core_api" in reports
    assert "feature_recommendation" in reports
    assert "feature_image_processing" in reports
    
    graph_str = StaticDependencyAnalyzer.generate_ascii_graph(reports)
    assert "[core_api]" in graph_str
    assert "indispensable" in graph_str

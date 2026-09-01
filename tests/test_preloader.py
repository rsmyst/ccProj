import pytest
import sys
from src.preloader import ModulePreloader

def test_preloader_operations():
    preloader = ModulePreloader()
    
    # Ensure module is cleared first
    if "math" in sys.modules:
        pass # standard library is always there
        
    preloader.preload(["src.workloads.auth_db"])
    assert "src.workloads.auth_db" in sys.modules
    
    preloader.evict(["src.workloads.auth_db"])
    assert "src.workloads.auth_db" not in sys.modules

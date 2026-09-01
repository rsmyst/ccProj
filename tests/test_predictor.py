import pytest
from src.predictor import TransitionPredictor

def test_predictor_transitions():
    p = TransitionPredictor()
    
    # Simulate A -> B (3 times), A -> C (1 time)
    p.record_transition("A", "B")
    p.record_transition("A", "B")
    p.record_transition("A", "B")
    p.record_transition("A", "C")
    
    preds = p.predict_next("A", top_k=1)
    assert len(preds) == 1
    assert preds[0][0] == "B"
    assert preds[0][1] == 0.75

def test_predictor_evaluation():
    p = TransitionPredictor()
    p.record_transition("A", "B")
    
    # Next time from A, predicting B should hit
    hit = p.evaluate_and_record("A", "B")
    assert hit is True
    
    # From B to C (no prior transition from B)
    hit_miss = p.evaluate_and_record("B", "C")
    assert hit_miss is False
    assert p.accuracy > 0

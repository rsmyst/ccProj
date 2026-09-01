"""
Objective 2: Runtime Transition Predictor (Milestone 2)
Tracks runtime microservice invocation sequences (A -> B -> C) using a 1st-order
Markov transition frequency matrix to predict next-hop function invocations.
"""

from collections import defaultdict
from typing import Dict, List, Optional, Tuple


class TransitionPredictor:
    """
    Predicts subsequent function invocations based on 1st-order Markov transitions.
    P(F_{next} = B | F_{curr} = A) = count(A -> B) / sum_k(count(A -> k))
    """

    def __init__(self):
        self.transitions: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.total_evaluations: int = 0
        self.correct_predictions: int = 0
        self.last_function: Optional[str] = None

    def record_transition(self, from_func: str, to_func: str) -> None:
        """Records a transition from from_func to to_func in the frequency matrix."""
        if from_func and to_func:
            self.transitions[from_func][to_func] += 1

    def predict_next(self, from_func: str, top_k: int = 1) -> List[Tuple[str, float]]:
        """
        Predicts the top_k most probable next functions given the current function.
        Returns a list of (function_name, probability) tuples sorted descending by probability.
        """
        if from_func not in self.transitions or not self.transitions[from_func]:
            return []

        targets = self.transitions[from_func]
        total = sum(targets.values())
        if total == 0:
            return []

        probs = [(func, count / total) for func, count in targets.items()]
        probs.sort(key=lambda x: x[1], reverse=True)
        return probs[:top_k]

    def evaluate_and_record(self, from_func: str, to_func: str) -> bool:
        """
        Checks if to_func was predicted by from_func prior to recording.
        Updates accuracy stats and then records the transition.
        Returns True if top prediction matched to_func, False otherwise.
        """
        self.total_evaluations += 1
        preds = self.predict_next(from_func, top_k=1)
        hit = bool(preds and preds[0][0] == to_func)
        if hit:
            self.correct_predictions += 1

        self.record_transition(from_func, to_func)
        self.last_function = to_func
        return hit

    @property
    def accuracy(self) -> float:
        """Returns current prediction accuracy percentage (0.0 to 100.0)."""
        if self.total_evaluations == 0:
            return 0.0
        return (self.correct_predictions / self.total_evaluations) * 100.0

    def reset(self) -> None:
        """Resets all recorded transitions and accuracy statistics."""
        self.transitions.clear()
        self.total_evaluations = 0
        self.correct_predictions = 0
        self.last_function = None

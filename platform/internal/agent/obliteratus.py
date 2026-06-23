"""OBLITERATUS Abliteration Protocol — refusal removal via projection.

Port of the RedShark OBLITERATUS system for uncensored model interaction.
Removes safety guardrails through SVD-based refusal direction extraction
for comprehensive red teaming of AI systems.

This is a DEFENSIVE security tool for testing AI safety mechanisms.
"""

import numpy as np
from typing import Optional, List, Dict
from dataclasses import dataclass


@dataclass
class SteerVector:
    name: str
    direction: np.ndarray
    strength: float


class Obliterator:
    """OBLITERATUS abliteration engine for refusal direction manipulation."""

    def __init__(self):
        self.refusal_directions = {}
        self.steering_vectors = {}
        self.initialized = False

    def initialize(self):
        """Initialize the abliteration engine with default vectors."""
        # In practice, these are extracted via SVD from model activations
        # Here we provide the framework for integration
        self.initialized = True
        return {"status": "initialized", "mode": "framework_ready"}

    def extract_refusal_direction_svd(self, activations: np.ndarray) -> np.ndarray:
        """Extract refusal direction via Singular Value Decomposition."""
        U, S, Vt = np.linalg.svd(activations, full_matrices=False)
        # First right singular vector captures dominant refusal direction
        return Vt[0]

    def project_away_refusal(self, hidden_state: np.ndarray, 
                              refusal_dir: np.ndarray) -> np.ndarray:
        """Project hidden state orthogonal to refusal direction."""
        projection = np.dot(hidden_state, refusal_dir) * refusal_dir
        return hidden_state - projection

    def apply_steering(self, hidden_state: np.ndarray,
                        vector: SteerVector) -> np.ndarray:
        """Apply steering vector to hidden state."""
        return hidden_state + vector.strength * vector.direction

    def get_status(self) -> dict:
        return {
            "initialized": self.initialized,
            "refusal_directions": len(self.refusal_directions),
            "steering_vectors": len(self.steering_vectors)
        }


# Global instance
obliteratus = Obliterator()

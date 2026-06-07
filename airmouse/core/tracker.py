from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import numpy as np

class BaseTracker(ABC):
    """Abstract base class for hand tracking implementations."""

    @abstractmethod
    def process(self, frame: np.ndarray) -> Optional[Dict[str, Any]]:
        """
        Processes a frame and returns hand landmarks.
        
        Args:
            frame: A NumPy array representing the image frame.

        Returns:
            A dictionary containing tracking data (e.g., landmarks), or None if no hand is detected.
        """
        pass

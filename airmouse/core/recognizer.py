from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BaseRecognizer(ABC):
    """Abstract base class for gesture recognition."""

    @abstractmethod
    def recognize(self, tracking_data: Dict[str, Any]) -> Optional[str]:
        """
        Analyzes tracking data to recognize a gesture.

        Args:
            tracking_data: Data returned by a BaseTracker.

        Returns:
            The name of the recognized gesture (e.g., 'pinch'), or None.
        """
        pass

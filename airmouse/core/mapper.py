from abc import ABC, abstractmethod
from typing import Optional

class BaseMapper(ABC):
    """Abstract base class for mapping gestures to actions."""

    @abstractmethod
    def get_action(self, gesture_name: str) -> Optional[str]:
        """
        Maps a gesture name to an action name.

        Args:
            gesture_name: The recognized gesture name.

        Returns:
            The name of the corresponding action, or None if unmapped.
        """
        pass

    @abstractmethod
    def load_mapping(self) -> None:
        """Loads or reloads the gesture-to-action mappings from config."""
        pass

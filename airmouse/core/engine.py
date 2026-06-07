from abc import ABC, abstractmethod

class BaseEngine(ABC):
    """Abstract base class for the main AirMouse++ engine loop."""

    @abstractmethod
    def start(self) -> None:
        """Starts the main engine loop."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stops the engine loop gracefully."""
        pass

    @property
    @abstractmethod
    def is_running(self) -> bool:
        """Returns True if the engine is currently running."""
        pass

from abc import ABC, abstractmethod
from typing import Optional
import numpy as np

class BaseCamera(ABC):
    """Abstract base class for camera implementations."""

    @abstractmethod
    def start(self) -> bool:
        """Initializes and starts the camera. Returns True if successful."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Stops and releases the camera."""
        pass

    @abstractmethod
    def read_frame(self) -> Optional[np.ndarray]:
        """Reads a single frame from the camera. Returns None if failed."""
        pass

    @property
    @abstractmethod
    def is_running(self) -> bool:
        """Returns True if the camera is currently running."""
        pass

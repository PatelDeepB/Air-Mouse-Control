import cv2
import numpy as np
from typing import Optional
import threading

from airmouse.core.camera import BaseCamera
from airmouse.utils.logger import setup_logger

logger = setup_logger("camera")

class OpenCVCamera(BaseCamera):
    """Camera implementation using OpenCV, reading frames in a separate thread."""

    def __init__(self, camera_index: int = 0, width: int = 640, height: int = 480):
        self.camera_index = camera_index
        self.width = width
        self.height = height
        self.cap: Optional[cv2.VideoCapture] = None
        
        self._running = False
        self._frame: Optional[np.ndarray] = None
        self._lock = threading.Lock()
        self._thread: Optional[threading.Thread] = None

    def start(self) -> bool:
        self.cap = cv2.VideoCapture(self.camera_index)
        if not self.cap.isOpened():
            logger.error(f"Failed to open camera index {self.camera_index}")
            return False
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        self._running = True
        self._thread = threading.Thread(target=self._update, daemon=True)
        self._thread.start()
        logger.info("Camera started successfully.")
        return True

    def _update(self) -> None:
        """Background thread that continuously reads frames from the camera."""
        while self._running and self.cap:
            ret, frame = self.cap.read()
            if ret:
                # Flip the frame horizontally for a selfie-view display
                frame = cv2.flip(frame, 1)
                with self._lock:
                    self._frame = frame
            else:
                logger.warning("Failed to grab frame.")

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)
        
        if self.cap:
            self.cap.release()
            self.cap = None
        logger.info("Camera stopped.")

    def read_frame(self) -> Optional[np.ndarray]:
        with self._lock:
            if self._frame is not None:
                return self._frame.copy()
        return None

    @property
    def is_running(self) -> bool:
        return self._running

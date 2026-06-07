import cv2
import time
from typing import Optional

from airmouse.core.engine import BaseEngine
from airmouse.core.camera import BaseCamera
from airmouse.core.tracker import BaseTracker
from airmouse.utils.logger import setup_logger

logger = setup_logger("engine")

class MainEngine(BaseEngine):
    """Main execution loop for AirMouse++."""

    def __init__(self, camera: BaseCamera, tracker: BaseTracker):
        self.camera = camera
        self.tracker = tracker
        self._running = False

    def start(self) -> None:
        if not self.camera.start():
            logger.error("Engine failed to start because camera could not be initialized.")
            return

        self._running = True
        logger.info("AirMouse++ Engine started. Press 'q' to quit.")
        self._run_loop()

    def _run_loop(self) -> None:
        prev_time = 0.0

        while self._running:
            frame = self.camera.read_frame()
            if frame is None:
                continue

            # Process frame for hand tracking
            tracking_data = self.tracker.process(frame)
            if tracking_data:
                # For now, just draw landmarks
                if hasattr(self.tracker, "draw_landmarks"):
                    self.tracker.draw_landmarks(frame, tracking_data)
                
            # Calculate FPS
            current_time = time.time()
            fps = 1 / (current_time - prev_time) if prev_time > 0 else 0
            prev_time = current_time

            # Overlay FPS
            cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Display the frame
            cv2.imshow("AirMouse++", frame)

            # Exit condition
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop()

    def stop(self) -> None:
        logger.info("Stopping AirMouse++ Engine...")
        self._running = False
        self.camera.stop()
        cv2.destroyAllWindows()

    @property
    def is_running(self) -> bool:
        return self._running

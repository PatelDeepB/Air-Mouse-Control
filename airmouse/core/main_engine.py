import cv2
import time
from typing import Optional

from airmouse.core.engine import BaseEngine
from airmouse.core.camera import BaseCamera
from airmouse.core.tracker import BaseTracker
from airmouse.core.recognizer import BaseRecognizer
from airmouse.core.mapper import BaseMapper
from airmouse.core.dispatcher import BaseDispatcher
from airmouse.core.plugin_manager import PluginManager
from airmouse.utils.logger import setup_logger

logger = setup_logger("engine")

class MainEngine(BaseEngine):
    """Main execution loop for AirMouse++."""

    def __init__(self, camera: BaseCamera, tracker: BaseTracker, recognizer: BaseRecognizer, mapper: BaseMapper, dispatcher: BaseDispatcher):
        self.camera = camera
        self.tracker = tracker
        self.recognizer = recognizer
        self.mapper = mapper
        self.dispatcher = dispatcher
        self._running = False
        self._prev_gesture: Optional[str] = None
        
        # Initialize and load plugins
        self.plugin_manager = PluginManager()
        self.plugin_manager.load_plugins()
        self.plugin_manager.register_to_dispatcher(self.dispatcher)

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
                
                # Recognize gesture
                gesture = self.recognizer.recognize(tracking_data)
                if gesture:
                    cv2.putText(frame, f"Gesture: {gesture}", (10, 70), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    
                    # Map gesture to action
                    action_name = self.mapper.get_action(gesture)
                    if action_name:
                        logger.info(f"Recognized gesture: {gesture} -> mapped to action: {action_name}")
                        # Dispatch action
                        # Some actions need coordinates (like mouse move), let's pass them
                        # We use the wrist or index tip as the cursor coordinate.
                        index_tip = tracking_data["landmarks"][8]
                        # Use pyautogui to get actual screen size
                        import pyautogui
                        screen_width, screen_height = pyautogui.size()
                        
                        # Active area bounding box: only the middle 60% of the camera maps to the full screen.
                        # This prevents the user from having to stretch their arm to the edges of the camera view.
                        margin_x, margin_y = 0.2, 0.2
                        
                        clamped_x = max(margin_x, min(1.0 - margin_x, index_tip["x"]))
                        clamped_y = max(margin_y, min(1.0 - margin_y, index_tip["y"]))
                        
                        normalized_x = (clamped_x - margin_x) / (1.0 - 2 * margin_x)
                        normalized_y = (clamped_y - margin_y) / (1.0 - 2 * margin_y)
                        
                        target_x = normalized_x * screen_width
                        target_y = normalized_y * screen_height
                        
                        # Edge-triggering logic: Continuous actions fire every frame.
                        # Discrete actions (clicks, play/pause) fire ONLY when the gesture first begins.
                        CONTINUOUS_ACTIONS = {"move", "drag", "scroll"}
                        is_continuous = action_name in CONTINUOUS_ACTIONS
                        is_new_gesture = gesture != self._prev_gesture
                        
                        if is_continuous or is_new_gesture:
                            self.dispatcher.dispatch(action_name, target_x=target_x, target_y=target_y, is_new_gesture=is_new_gesture)
                            
                    self._prev_gesture = gesture

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

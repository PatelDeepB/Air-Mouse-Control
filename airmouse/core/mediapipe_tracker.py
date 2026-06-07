import cv2
import mediapipe as mp
import numpy as np
from typing import Any, Dict, Optional, List

from airmouse.core.tracker import BaseTracker

class MediaPipeTracker(BaseTracker):
    """Hand tracker implementation using Google's MediaPipe."""

    def __init__(self, max_num_hands: int = 1, min_detection_confidence: float = 0.7, min_tracking_confidence: float = 0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils

    def process(self, frame: np.ndarray) -> Optional[Dict[str, Any]]:
        # Convert the BGR image to RGB before processing
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # To improve performance, optionally mark the image as not writeable to pass by reference
        rgb_frame.flags.writeable = False
        results = self.hands.process(rgb_frame)
        rgb_frame.flags.writeable = True

        if not results.multi_hand_landmarks:
            return None

        # We will parse the first detected hand
        # We can expand this to multi-hand tracking if needed
        hand_landmarks = results.multi_hand_landmarks[0]
        handedness = results.multi_handedness[0].classification[0].label

        # Convert landmarks to a list of dicts with x, y, z normalized coordinates
        landmarks = []
        for lm in hand_landmarks.landmark:
            landmarks.append({
                "x": lm.x,
                "y": lm.y,
                "z": lm.z
            })

        return {
            "landmarks": landmarks,
            "handedness": handedness,
            "raw_landmarks": hand_landmarks  # Store raw MediaPipe object for drawing
        }

    def draw_landmarks(self, frame: np.ndarray, tracking_data: Dict[str, Any]) -> None:
        """Helper method to visualize the landmarks on the frame."""
        if tracking_data and "raw_landmarks" in tracking_data:
            self.mp_draw.draw_landmarks(
                frame, 
                tracking_data["raw_landmarks"], 
                self.mp_hands.HAND_CONNECTIONS
            )

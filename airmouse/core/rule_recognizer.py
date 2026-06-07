import math
from typing import Any, Dict, Optional, List
from collections import deque, Counter

from airmouse.core.recognizer import BaseRecognizer

class RuleRecognizer(BaseRecognizer):
    """Rule-based gesture recognizer using MediaPipe landmarks."""

    def __init__(self, confidence_threshold: float = 0.6, smoothing_window: int = 3):
        self.confidence_threshold = confidence_threshold
        # Smoothing window stores the last N gestures
        self.history = deque(maxlen=smoothing_window)

    def _distance(self, p1: Dict[str, float], p2: Dict[str, float]) -> float:
        """Calculates Euclidean distance between two 3D landmarks."""
        return math.sqrt((p1["x"] - p2["x"])**2 + (p1["y"] - p2["y"])**2 + (p1["z"] - p2["z"])**2)

    def _is_finger_extended(self, landmarks: List[Dict[str, float]], tip_idx: int, pip_idx: int, wrist_idx: int = 0) -> bool:
        """Determines if a finger is extended by comparing distance to wrist."""
        dist_tip = self._distance(landmarks[tip_idx], landmarks[wrist_idx])
        dist_pip = self._distance(landmarks[pip_idx], landmarks[wrist_idx])
        # If the tip is significantly further from the wrist than the PIP joint, it's extended
        return dist_tip > dist_pip * 1.1

    def recognize(self, tracking_data: Dict[str, Any]) -> Optional[str]:
        if not tracking_data or "landmarks" not in tracking_data:
            self.history.append(None)
            return None

        landmarks = tracking_data["landmarks"]
        gesture = self._detect_gesture(landmarks)
        
        self.history.append(gesture)
        return self._smooth_gesture()

    def _detect_gesture(self, landmarks: List[Dict[str, float]]) -> str:
        # Landmark Indices
        # 0: Wrist
        # 4: Thumb tip, 3: Thumb IP, 2: Thumb MCP
        # 8: Index tip, 6: Index PIP
        # 12: Middle tip, 10: Middle PIP
        # 16: Ring tip, 14: Ring PIP
        # 20: Pinky tip, 18: Pinky PIP
        
        thumb_extended = self._is_finger_extended(landmarks, 4, 3)
        index_extended = self._is_finger_extended(landmarks, 8, 6)
        middle_extended = self._is_finger_extended(landmarks, 12, 10)
        ring_extended = self._is_finger_extended(landmarks, 16, 14)
        pinky_extended = self._is_finger_extended(landmarks, 20, 18)

        fingers_extended = [thumb_extended, index_extended, middle_extended, ring_extended, pinky_extended]
        extended_count = sum(fingers_extended)

        # Pinch detection: Thumb and Index close together
        thumb_index_dist = self._distance(landmarks[4], landmarks[8])
        thumb_middle_dist = self._distance(landmarks[4], landmarks[12])
        
        is_double_pinch = thumb_index_dist < 0.08 and thumb_middle_dist < 0.08 and not ring_extended and not pinky_extended
        # Normalized distance threshold for single pinch
        is_pinch = thumb_index_dist < 0.08 and not is_double_pinch and not middle_extended and not ring_extended

        if is_double_pinch:
            return "double_pinch"

        if is_pinch:
            return "pinch"

        if index_extended and not thumb_extended and not middle_extended and not ring_extended and not pinky_extended:
            return "point"

        if extended_count == 5:
            return "open_palm"
            
        if extended_count <= 1 and not thumb_extended and not index_extended:
            return "fist"
            
        if index_extended and middle_extended and not thumb_extended and not ring_extended and not pinky_extended:
            return "peace"

        if thumb_extended and not index_extended and not middle_extended and not ring_extended and not pinky_extended:
            # Thumb Y is smaller if pointing UP (since image origin is top-left)
            if landmarks[4]["y"] < landmarks[0]["y"]:
                return "thumb_up"
            else:
                return "thumb_down"

        return "unknown"

    def _smooth_gesture(self) -> Optional[str]:
        """Returns the most common gesture in the window if it meets the confidence threshold."""
        valid_history = [g for g in self.history if g is not None and g != "unknown"]
        if not valid_history:
            return None
            
        counter = Counter(valid_history)
        most_common, count = counter.most_common(1)[0]
        
        confidence = count / self.history.maxlen
        
        if confidence >= self.confidence_threshold:
            return most_common
            
        return None

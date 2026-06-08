import os
import joblib
import numpy as np
from typing import Any, Dict, Optional, List
from collections import deque, Counter

from airmouse.core.recognizer import BaseRecognizer
from airmouse.core.rule_recognizer import RuleRecognizer
from airmouse.utils.logger import setup_logger

logger = setup_logger("ml_recognizer")

class MLRecognizer(BaseRecognizer):
    """Machine Learning based gesture recognizer using a custom trained model.
    Falls back to RuleRecognizer if the model is missing.
    """

    def __init__(self, model_path: str = "custom_gestures.pkl", confidence_threshold: float = 0.6, smoothing_window: int = 3):
        self.confidence_threshold = confidence_threshold
        self.history = deque(maxlen=smoothing_window)
        
        self.model = None
        self.fallback = None
        
        if os.path.exists(model_path):
            try:
                self.model = joblib.load(model_path)
                logger.info(f"Loaded custom ML gesture model from {model_path}")
            except Exception as e:
                logger.error(f"Failed to load ML model {model_path}: {e}")
                self.fallback = RuleRecognizer(confidence_threshold, smoothing_window)
        else:
            logger.warning(f"ML model {model_path} not found. Run 'airmouse train' to calibrate. Falling back to RuleRecognizer.")
            self.fallback = RuleRecognizer(confidence_threshold, smoothing_window)

    def _flatten_landmarks(self, landmarks: List[Dict[str, float]]) -> np.ndarray:
        flattened = []
        for lm in landmarks:
            flattened.extend([lm["x"], lm["y"], lm["z"]])
        return np.array(flattened).reshape(1, -1)

    def recognize(self, tracking_data: Dict[str, Any]) -> Optional[str]:
        if self.fallback:
            return self.fallback.recognize(tracking_data)
            
        if not tracking_data or "landmarks" not in tracking_data:
            self.history.append(None)
            return None

        features = self._flatten_landmarks(tracking_data["landmarks"])
        
        try:
            # Predict
            pred = self.model.predict(features)[0]
            # Get probabilities
            probs = self.model.predict_proba(features)[0]
            max_prob = np.max(probs)
            
            # If the ML model itself has low confidence, return unknown
            if max_prob < 0.4:
                gesture = "unknown"
            else:
                gesture = str(pred)
        except Exception as e:
            logger.error(f"ML Prediction failed: {e}")
            gesture = "unknown"
            
        self.history.append(gesture)
        return self._smooth_gesture()

    def _smooth_gesture(self) -> Optional[str]:
        valid_history = [g for g in self.history if g is not None and g != "unknown"]
        if not valid_history:
            return None
            
        counter = Counter(valid_history)
        most_common, count = counter.most_common(1)[0]
        
        confidence = count / self.history.maxlen
        
        if confidence >= self.confidence_threshold:
            return most_common
            
        return None

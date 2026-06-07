import os
import joblib
import numpy as np
from typing import Any, Dict, Optional, List
from collections import deque, Counter

from airmouse.core.recognizer import BaseRecognizer
from airmouse.utils.logger import setup_logger

logger = setup_logger("ml_recognizer")

class MLRecognizer(BaseRecognizer):
    """Machine learning based recognizer using a trained model."""

    def __init__(self, model_path: str = "custom_gestures.pkl", confidence_threshold: float = 0.7, smoothing_window: int = 5):
        self.model_path = model_path
        self.confidence_threshold = confidence_threshold
        self.history = deque(maxlen=smoothing_window)
        self.model = None
        self._load_model()

    def _load_model(self):
        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                logger.info(f"Loaded custom gesture model from {self.model_path}")
            except Exception as e:
                logger.error(f"Failed to load model from {self.model_path}: {e}")
        else:
            logger.warning(f"Model file not found at {self.model_path}. ML recognition disabled until trained.")

    def _flatten_landmarks(self, landmarks: List[Dict[str, float]]) -> np.ndarray:
        flattened = []
        for lm in landmarks:
            flattened.extend([lm["x"], lm["y"], lm["z"]])
        return np.array(flattened).reshape(1, -1)

    def recognize(self, tracking_data: Dict[str, Any]) -> Optional[str]:
        if not self.model or not tracking_data or "landmarks" not in tracking_data:
            self.history.append(None)
            return None

        landmarks = tracking_data["landmarks"]
        features = self._flatten_landmarks(landmarks)
        
        try:
            # For KNN, predict returns the class. 
            # predict_proba returns probabilities if we wanted finer confidence.
            prediction = self.model.predict(features)[0]
            self.history.append(prediction)
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            self.history.append(None)

        return self._smooth_gesture()

    def _smooth_gesture(self) -> Optional[str]:
        valid_history = [g for g in self.history if g is not None]
        if not valid_history:
            return None
            
        counter = Counter(valid_history)
        most_common, count = counter.most_common(1)[0]
        
        confidence = count / self.history.maxlen
        
        if confidence >= self.confidence_threshold:
            return most_common
            
        return None

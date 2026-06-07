import os
import joblib
import numpy as np
from typing import List, Dict, Tuple, Any
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from airmouse.utils.logger import setup_logger

logger = setup_logger("gesture_trainer")

class GestureTrainer:
    """Records landmarks and trains a custom gesture classifier."""

    def __init__(self, model_path: str = "custom_gestures.pkl"):
        self.model_path = model_path
        self.dataset_X: List[np.ndarray] = []
        self.dataset_y: List[str] = []

    def flatten_landmarks(self, landmarks: List[Dict[str, float]]) -> np.ndarray:
        """Flattens 3D landmarks into a 1D array for ML model."""
        flattened = []
        for lm in landmarks:
            flattened.extend([lm["x"], lm["y"], lm["z"]])
        return np.array(flattened)

    def add_sample(self, landmarks: List[Dict[str, float]], label: str) -> None:
        """Adds a single frame of landmarks to the training dataset."""
        features = self.flatten_landmarks(landmarks)
        self.dataset_X.append(features)
        self.dataset_y.append(label)

    def train_and_save(self) -> bool:
        """Trains a KNN model on collected data and saves it."""
        if len(self.dataset_X) < 10:
            logger.error("Not enough data to train. Please collect more frames.")
            return False

        logger.info(f"Training model on {len(self.dataset_X)} samples...")
        
        X = np.array(self.dataset_X)
        y = np.array(self.dataset_y)

        # Basic K-Nearest Neighbors Classifier
        model = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=3))
        model.fit(X, y)

        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(self.model_path)) or ".", exist_ok=True)
        
        joblib.dump(model, self.model_path)
        logger.info(f"Model successfully saved to {self.model_path}")
        return True

    def clear_dataset(self) -> None:
        """Clears the currently collected data in memory."""
        self.dataset_X = []
        self.dataset_y = []

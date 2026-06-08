import os
from airmouse.gestures.trainer import GestureTrainer
from airmouse.gestures.classifier import MLRecognizer

def test_trainer_and_classifier(tmp_path):
    model_file = str(tmp_path / "test_model.pkl")
    
    # 1. Train model
    trainer = GestureTrainer(model_path=model_file)
    
    # Create fake landmarks for "gesture_a"
    landmarks_a = [{"x": 0.1, "y": 0.1, "z": 0.1}] * 21
    # Create fake landmarks for "gesture_b"
    landmarks_b = [{"x": 0.9, "y": 0.9, "z": 0.9}] * 21
    
    for _ in range(15):
        trainer.add_sample(landmarks_a, "gesture_a")
        trainer.add_sample(landmarks_b, "gesture_b")
        
    assert len(trainer.dataset_X) == 30
    assert trainer.train_and_save() is True
    assert os.path.exists(model_file)
    
    # 2. Test inference
    recognizer = MLRecognizer(model_path=model_file, confidence_threshold=0.1, smoothing_window=1)
    
    result_a = recognizer.recognize({"landmarks": landmarks_a})
    assert result_a == "gesture_a"
    
    result_b = recognizer.recognize({"landmarks": landmarks_b})
    assert result_b == "gesture_b"

def test_classifier_no_model():
    recognizer = MLRecognizer(model_path="non_existent_model.pkl")
    assert recognizer.model is None
    result = recognizer.recognize({"landmarks": [{"x": 0, "y": 0, "z": 0}] * 21})
    assert result is None

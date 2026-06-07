from airmouse.core.rule_recognizer import RuleRecognizer

def test_recognizer_initialization():
    recognizer = RuleRecognizer(confidence_threshold=0.6, smoothing_window=3)
    assert recognizer.confidence_threshold == 0.6
    assert recognizer.history.maxlen == 3

def test_recognize_open_palm():
    recognizer = RuleRecognizer(confidence_threshold=0.1, smoothing_window=1)
    # Mock landmarks for open palm
    # All fingers extended (tips further from wrist than PIPs)
    landmarks = [{"x": 0.5, "y": 0.8, "z": 0}] * 21  # Default to base/wrist positions
    landmarks[0] = {"x": 0.5, "y": 0.8, "z": 0.0} # Wrist
    
    # Thumb
    landmarks[2] = {"x": 0.4, "y": 0.7, "z": 0}
    landmarks[3] = {"x": 0.3, "y": 0.6, "z": 0}
    landmarks[4] = {"x": 0.2, "y": 0.5, "z": 0} # Tip extended far left/up
    
    # Index
    landmarks[5] = {"x": 0.4, "y": 0.6, "z": 0}
    landmarks[6] = {"x": 0.4, "y": 0.5, "z": 0}
    landmarks[8] = {"x": 0.4, "y": 0.3, "z": 0} # Tip extended far up
    
    # Middle
    landmarks[9] = {"x": 0.5, "y": 0.6, "z": 0}
    landmarks[10] = {"x": 0.5, "y": 0.5, "z": 0}
    landmarks[12] = {"x": 0.5, "y": 0.2, "z": 0} # Tip extended far up
    
    # Ring
    landmarks[13] = {"x": 0.6, "y": 0.6, "z": 0}
    landmarks[14] = {"x": 0.6, "y": 0.5, "z": 0}
    landmarks[16] = {"x": 0.6, "y": 0.3, "z": 0} # Tip extended far up
    
    # Pinky
    landmarks[17] = {"x": 0.7, "y": 0.6, "z": 0}
    landmarks[18] = {"x": 0.7, "y": 0.5, "z": 0}
    landmarks[20] = {"x": 0.7, "y": 0.4, "z": 0} # Tip extended far up right

    tracking_data = {"landmarks": landmarks}
    result = recognizer.recognize(tracking_data)
    assert result == "open_palm"

def test_recognize_pinch():
    recognizer = RuleRecognizer(confidence_threshold=0.1, smoothing_window=1)
    
    landmarks = [{"x": 0.5, "y": 0.8, "z": 0}] * 21
    landmarks[0] = {"x": 0.5, "y": 0.8, "z": 0.0} # Wrist
    
    # Pinch: Thumb and Index tips close to each other
    landmarks[4] = {"x": 0.5, "y": 0.5, "z": 0}
    landmarks[8] = {"x": 0.51, "y": 0.51, "z": 0} # Very close to thumb tip
    
    # Ensure they are "extended" enough from wrist
    landmarks[3] = {"x": 0.4, "y": 0.6, "z": 0}
    landmarks[6] = {"x": 0.6, "y": 0.6, "z": 0}

    tracking_data = {"landmarks": landmarks}
    result = recognizer.recognize(tracking_data)
    assert result == "pinch"

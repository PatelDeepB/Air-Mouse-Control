import numpy as np
import pytest
from unittest.mock import MagicMock, patch

from airmouse.core.opencv_camera import OpenCVCamera
from airmouse.core.mediapipe_tracker import MediaPipeTracker
from airmouse.core.main_engine import MainEngine

def test_camera_initialization():
    camera = OpenCVCamera()
    assert camera.is_running is False
    assert camera.camera_index == 0
    assert camera.width == 640
    assert camera.height == 480

@patch("cv2.VideoCapture")
def test_camera_start_stop(mock_video_capture):
    mock_cap = MagicMock()
    mock_cap.isOpened.return_value = True
    mock_cap.read.return_value = (True, np.zeros((480, 640, 3), dtype=np.uint8))
    mock_video_capture.return_value = mock_cap

    camera = OpenCVCamera()
    assert camera.start() is True
    assert camera.is_running is True
    
    camera.stop()
    assert camera.is_running is False
    mock_cap.release.assert_called_once()

def test_tracker_initialization():
    tracker = MediaPipeTracker()
    assert tracker is not None

@patch("mediapipe.solutions.hands.Hands")
def test_tracker_process_no_hands(mock_hands):
    # Mock hands to return no landmarks
    mock_process_result = MagicMock()
    mock_process_result.multi_hand_landmarks = None
    mock_hands.return_value.process.return_value = mock_process_result

    tracker = MediaPipeTracker()
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    result = tracker.process(frame)
    assert result is None

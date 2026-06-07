import pytest
from airmouse.config.settings import CameraSettings, RecognizerSettings, Settings

def test_settings_defaults():
    settings = Settings()
    assert settings.camera.fps == 30
    assert settings.camera.width == 640
    assert settings.camera.height == 480
    assert settings.recognizer.confidence_threshold == 0.7

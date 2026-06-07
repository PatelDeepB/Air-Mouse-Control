from pydantic import BaseModel
import yaml
from typing import Dict
from pathlib import Path

class CameraSettings(BaseModel):
    index: int = 0
    width: int = 640
    height: int = 480
    fps: int = 30

class RecognizerSettings(BaseModel):
    confidence_threshold: float = 0.7
    smoothing_factor: float = 0.5

class Settings(BaseModel):
    camera: CameraSettings = CameraSettings()
    recognizer: RecognizerSettings = RecognizerSettings()
    gestures: Dict[str, str] = {}  # gesture_name -> action_name

def load_settings(config_path: str) -> Settings:
    """Loads configuration from a YAML file.

    Args:
        config_path: Path to the YAML configuration file.

    Returns:
        A Settings object populated with data from the config file, or defaults if not found.
    """
    path = Path(config_path)
    if not path.exists():
        return Settings()
    
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f) or {}
    return Settings(**data)

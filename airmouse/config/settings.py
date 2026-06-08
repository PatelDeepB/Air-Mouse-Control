from pydantic import BaseModel
import yaml
from typing import Dict
from pathlib import Path
from airmouse.utils.logger import setup_logger

logger = setup_logger("settings")

class CameraSettings(BaseModel):
    index: int = 0
    width: int = 640
    height: int = 480
    fps: int = 30
    comfort_margin_x: float = 0.2
    comfort_margin_y: float = 0.2

class RecognizerSettings(BaseModel):
    confidence_threshold: float = 0.7
    smoothing_factor: float = 0.5

class Settings(BaseModel):
    camera: CameraSettings = CameraSettings()
    recognizer: RecognizerSettings = RecognizerSettings()
    gestures: Dict[str, str] = {
        "point": "move",
        "pinch": "left_click_drag",
        "shaka": "right_click",
        "double_pinch": "double_click",
        "thumb_up": "scroll_up",
        "thumb_down": "scroll_down"
    }

def load_settings(config_path: str) -> Settings:
    """Loads configuration from a YAML file.

    Args:
        config_path: Path to the YAML configuration file.

    Returns:
        A Settings object populated with data from the config file, or defaults if not found.
    """
    path = Path(config_path)
    if not path.exists():
        logger.warning(f"Config file not found at {path.absolute()}. Using default settings.")
        return Settings()
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}
        return Settings(**data)
    except Exception as e:
        logger.error(f"Error loading config file: {e}. Using default settings.")
        return Settings()

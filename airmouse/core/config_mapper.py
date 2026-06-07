from typing import Dict, Optional
from airmouse.core.mapper import BaseMapper
from airmouse.config.settings import load_settings

class ConfigMapper(BaseMapper):
    """Maps gestures to actions using the YAML configuration."""

    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.mapping: Dict[str, str] = {}
        self.load_mapping()

    def get_action(self, gesture_name: str) -> Optional[str]:
        return self.mapping.get(gesture_name)

    def load_mapping(self) -> None:
        settings = load_settings(self.config_path)
        self.mapping = settings.gestures

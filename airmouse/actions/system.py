import pyautogui
from airmouse.utils.logger import setup_logger

logger = setup_logger("system_controller")

class SystemController:
    """Controls system volume and brightness."""

    def volume_up(self, steps: int = 2) -> None:
        for _ in range(steps):
            pyautogui.press('volumeup')

    def volume_down(self, steps: int = 2) -> None:
        for _ in range(steps):
            pyautogui.press('volumedown')

    def volume_mute(self) -> None:
        pyautogui.press('volumemute')

    def brightness_up(self) -> None:
        # Cross-platform brightness control often requires 3rd party packages
        # like `screen-brightness-control`. We will log a warning if not implemented.
        logger.warning("Brightness control requires an external library (e.g., screen-brightness-control).")

    def brightness_down(self) -> None:
        logger.warning("Brightness control requires an external library (e.g., screen-brightness-control).")

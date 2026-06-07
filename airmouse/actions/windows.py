import pyautogui
import platform

class WindowController:
    """Controls window management (minimize, maximize, alt-tab)."""

    def __init__(self):
        self.os_name = platform.system()

    def minimize(self) -> None:
        if self.os_name == "Windows":
            pyautogui.hotkey('win', 'down')
        elif self.os_name == "Darwin": # macOS
            pyautogui.hotkey('command', 'm')
        else: # Linux
            pyautogui.hotkey('ctrl', 'alt', 'd')

    def maximize(self) -> None:
        if self.os_name == "Windows":
            pyautogui.hotkey('win', 'up')
        elif self.os_name == "Darwin":
            pyautogui.hotkey('ctrl', 'command', 'f')
        else:
            pyautogui.hotkey('alt', 'f10')

    def switch_next(self) -> None:
        """Simulates Alt+Tab"""
        if self.os_name == "Darwin":
            pyautogui.hotkey('command', 'tab')
        else:
            pyautogui.hotkey('alt', 'tab')

    def switch_previous(self) -> None:
        """Simulates Alt+Shift+Tab"""
        if self.os_name == "Darwin":
            pyautogui.hotkey('command', 'shift', 'tab')
        else:
            pyautogui.hotkey('alt', 'shift', 'tab')

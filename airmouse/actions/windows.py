import pyautogui
import platform
from airmouse.actions.linux_uinput import uinput_manager

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
            if uinput_manager.is_active:
                uinput_manager.hotkey(uinput_manager.e.KEY_LEFTMETA, uinput_manager.e.KEY_DOWN)
            else:
                pyautogui.hotkey('ctrl', 'alt', 'd')

    def maximize(self) -> None:
        if self.os_name == "Windows":
            pyautogui.hotkey('win', 'up')
        elif self.os_name == "Darwin":
            pyautogui.hotkey('ctrl', 'command', 'f')
        else:
            if uinput_manager.is_active:
                uinput_manager.hotkey(uinput_manager.e.KEY_LEFTALT, uinput_manager.e.KEY_F10)
            else:
                pyautogui.hotkey('alt', 'f10')

    def switch_next(self) -> None:
        """Simulates Alt+Tab"""
        if self.os_name == "Darwin":
            pyautogui.hotkey('command', 'tab')
        else:
            if self.os_name == "Linux" and uinput_manager.is_active:
                uinput_manager.hotkey(uinput_manager.e.KEY_LEFTALT, uinput_manager.e.KEY_TAB)
            else:
                pyautogui.hotkey('alt', 'tab')

    def switch_previous(self) -> None:
        """Simulates Alt+Shift+Tab"""
        if self.os_name == "Darwin":
            pyautogui.hotkey('command', 'shift', 'tab')
        else:
            if self.os_name == "Linux" and uinput_manager.is_active:
                uinput_manager.hotkey(uinput_manager.e.KEY_LEFTALT, uinput_manager.e.KEY_LEFTSHIFT, uinput_manager.e.KEY_TAB)
            else:
                pyautogui.hotkey('alt', 'shift', 'tab')

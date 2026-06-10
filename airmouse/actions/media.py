import pyautogui
from airmouse.actions.linux_uinput import uinput_manager

class MediaController:
    """Controls media playback using virtual keyboard keys."""

    def play_pause(self) -> None:
        if uinput_manager.is_active:
            uinput_manager.press_key(uinput_manager.e.KEY_PLAYPAUSE)
        else:
            pyautogui.press('playpause')

    def next_track(self) -> None:
        if uinput_manager.is_active:
            uinput_manager.press_key(uinput_manager.e.KEY_NEXTSONG)
        else:
            pyautogui.press('nexttrack')

    def previous_track(self) -> None:
        if uinput_manager.is_active:
            uinput_manager.press_key(uinput_manager.e.KEY_PREVIOUSSONG)
        else:
            pyautogui.press('prevtrack')

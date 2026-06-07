import pyautogui

class MediaController:
    """Controls media playback using virtual keyboard keys."""

    def play_pause(self) -> None:
        pyautogui.press('playpause')

    def next_track(self) -> None:
        pyautogui.press('nexttrack')

    def previous_track(self) -> None:
        pyautogui.press('prevtrack')

import pyautogui
from pynput.mouse import Controller, Button
import time

class MouseController:
    """Controls mouse movement, clicking, and scrolling."""

    def __init__(self, smoothing_factor: float = 0.5):
        self.mouse = Controller()
        self.smoothing_factor = smoothing_factor
        self.prev_x, self.prev_y = self.mouse.position
        
        # PyAutoGUI settings
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0.0

    def move(self, target_x: float, target_y: float) -> None:
        """Moves the mouse with smoothing applied."""
        # Exponential moving average for smoothing
        smooth_x = self.prev_x + (target_x - self.prev_x) * self.smoothing_factor
        smooth_y = self.prev_y + (target_y - self.prev_y) * self.smoothing_factor

        self.mouse.position = (smooth_x, smooth_y)
        self.prev_x, self.prev_y = smooth_x, smooth_y

    def click(self, button: str = "left") -> None:
        if button == "left":
            self.mouse.click(Button.left)
        elif button == "right":
            self.mouse.click(Button.right)
        elif button == "middle":
            self.mouse.click(Button.middle)

    def double_click(self) -> None:
        self.mouse.click(Button.left, 2)

    def scroll(self, clicks: int) -> None:
        """Scrolls the mouse vertically. Positive is up, negative is down."""
        self.mouse.scroll(0, clicks)

    def drag(self, start_x: float, start_y: float, end_x: float, end_y: float) -> None:
        # Move to start
        self.mouse.position = (start_x, start_y)
        time.sleep(0.05)
        self.mouse.press(Button.left)
        time.sleep(0.05)
        
        # Move to end
        self.move(end_x, end_y)
        time.sleep(0.05)
        self.mouse.release(Button.left)

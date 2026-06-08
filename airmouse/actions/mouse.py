import pyautogui
from pynput.mouse import Controller, Button
import time

class MouseController:
    """Controls mouse movement, clicking, and scrolling."""

    def __init__(self, smoothing_factor: float = 0.7):
        self.mouse = Controller()
        self.smoothing_factor = smoothing_factor
        self.prev_x, self.prev_y = self.mouse.position
        self.last_click_time = 0.0
        
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

    def left_click(self) -> None:
        self.mouse.click(Button.left)
        
    def right_click(self) -> None:
        self.mouse.click(Button.right)
        
    def middle_click(self) -> None:
        self.mouse.click(Button.middle)

    def double_click(self) -> None:
        self.mouse.click(Button.left, 2)

    def scroll(self, target_y: float = 0.0, is_new_gesture: bool = False, **kwargs) -> None:
        """Scrolls the mouse vertically based on hand movement."""
        if is_new_gesture or not hasattr(self, 'prev_scroll_y'):
            self.prev_scroll_y = target_y
            return
            
        delta = target_y - self.prev_scroll_y
        
        # Threshold to avoid jitter. target_y is in screen coordinates (pixels).
        sensitivity = 30.0
        
        if abs(delta) > sensitivity:
            # delta < 0 means hand moved UP. pynput scroll UP is positive.
            clicks = -int(delta / sensitivity)
            self.mouse.scroll(0, clicks)
            
            # Reset reference point
            self.prev_scroll_y = target_y

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

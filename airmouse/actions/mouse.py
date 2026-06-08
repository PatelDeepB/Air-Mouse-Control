import pyautogui
from pynput.mouse import Controller, Button
import time
from airmouse.utils.filters import OneEuroFilter

class MouseController:
    """Controls mouse movement, clicking, and scrolling using a State Machine."""

    def __init__(self):
        self.mouse = Controller()
        self.last_click_time = 0.0
        
        self.filter_x = None
        self.filter_y = None
        
        # State variables
        self.is_left_pressed = False
        self.freeze_until = 0.0
        self.scroll_anchor = None
        
        # PyAutoGUI settings
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0.0

    def update_position(self, target_x: float, target_y: float) -> None:
        """Called every frame to update cursor absolutely, utilizing OneEuroFilter for zero jitter."""
        t = time.time()
        
        # Click stabilization: Don't move the mouse if we are in a click-freeze period.
        if t < self.freeze_until:
            # Re-initialize filters so it doesn't jump wildly after unfreezing
            self.filter_x = None
            self.filter_y = None
            return
            
        if self.filter_x is None:
            # First frame of movement (or after unfreezing)
            # Use strict min_cutoff to kill jitter at rest, and small beta to allow speed
            self.filter_x = OneEuroFilter(t, target_x, min_cutoff=0.01, beta=0.005)
            self.filter_y = OneEuroFilter(t, target_y, min_cutoff=0.01, beta=0.005)
            self.mouse.position = (target_x, target_y)
            return

        # Apply 1 Euro Filter to absolute coordinates
        smooth_x = self.filter_x(t, target_x)
        smooth_y = self.filter_y(t, target_y)

        self.mouse.position = (smooth_x, smooth_y)

    def set_left_click(self, pressed: bool) -> None:
        if pressed and not self.is_left_pressed:
            self._stabilize_click()
            self.mouse.press(Button.left)
            self.is_left_pressed = True
        elif not pressed and self.is_left_pressed:
            self.mouse.release(Button.left)
            self.is_left_pressed = False

    def trigger_right_click(self) -> None:
        self._stabilize_click()
        self.mouse.click(Button.right)

    def trigger_double_click(self) -> None:
        self._stabilize_click()
        self.mouse.click(Button.left, 2)

    def update_scroll(self, target_y: float, is_start: bool) -> None:
        """Scrolls the mouse vertically based on y position (legacy peace-sign scroll)."""
        if is_start or self.scroll_anchor is None:
            self.scroll_anchor = target_y
            return
            
        delta = target_y - self.scroll_anchor
        sensitivity = 40.0
        
        if abs(delta) > sensitivity:
            clicks = -int(delta / sensitivity)
            self.mouse.scroll(0, clicks)
            self.scroll_anchor = target_y

    def scroll_up(self, **kwargs) -> None:
        """Scrolls the mouse up continuously."""
        self.mouse.scroll(0, 1)

    def scroll_down(self, **kwargs) -> None:
        """Scrolls the mouse down continuously."""
        self.mouse.scroll(0, -1)

    def _stabilize_click(self) -> None:
        """Freezes the mouse for 0.4 seconds to prevent the cursor from slipping while pinching."""
        self.freeze_until = time.time() + 0.4

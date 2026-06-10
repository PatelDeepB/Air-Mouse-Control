import os
import platform

from airmouse.utils.logger import setup_logger

logger = setup_logger("linux_uinput")

class LinuxUInputManager:
    """Singleton manager for the Linux evdev UInput virtual device."""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LinuxUInputManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
            
        self.ui = None
        self.e = None
        
        if platform.system() == "Linux" and os.environ.get("WAYLAND_DISPLAY"):
            try:
                import evdev
                from evdev import UInput, ecodes, AbsInfo
                self.e = ecodes
                
                # Define capabilities for absolute mouse, buttons, and keys
                cap = {
                    self.e.EV_KEY: [
                        self.e.BTN_LEFT, self.e.BTN_RIGHT, self.e.BTN_MIDDLE,
                        self.e.KEY_VOLUMEUP, self.e.KEY_VOLUMEDOWN, self.e.KEY_MUTE,
                        self.e.KEY_PLAYPAUSE, self.e.KEY_NEXTSONG, self.e.KEY_PREVIOUSSONG,
                        self.e.KEY_LEFTMETA, self.e.KEY_DOWN, self.e.KEY_UP,
                        self.e.KEY_TAB, self.e.KEY_LEFTALT, self.e.KEY_LEFTSHIFT,
                        self.e.KEY_F10
                    ],
                    self.e.EV_ABS: [
                        (self.e.ABS_X, AbsInfo(value=0, min=0, max=1920, fuzz=0, flat=0, resolution=0)),
                        (self.e.ABS_Y, AbsInfo(value=0, min=0, max=1080, fuzz=0, flat=0, resolution=0))
                    ],
                    self.e.EV_REL: [
                        self.e.REL_WHEEL
                    ]
                }
                self.ui = UInput(cap, name="AirMouse-Virtual-Device")
                logger.info("Initialized evdev UInput for Wayland native control.")
            except ImportError:
                logger.error("evdev is not installed. Native Wayland support will fail.")
            except PermissionError:
                logger.error("Permission denied creating UInput device. Must run with sudo.")
                
        self._initialized = True

    @property
    def is_active(self) -> bool:
        return self.ui is not None

    def move_mouse_abs(self, x: int, y: int) -> None:
        if self.ui and self.e:
            self.ui.write(self.e.EV_ABS, self.e.ABS_X, int(x))
            self.ui.write(self.e.EV_ABS, self.e.ABS_Y, int(y))
            self.ui.syn()

    def set_button(self, button_code: int, pressed: bool) -> None:
        if self.ui and self.e:
            self.ui.write(self.e.EV_KEY, button_code, 1 if pressed else 0)
            self.ui.syn()

    def click_button(self, button_code: int) -> None:
        if self.ui and self.e:
            self.ui.write(self.e.EV_KEY, button_code, 1)
            self.ui.write(self.e.EV_KEY, button_code, 0)
            self.ui.syn()

    def press_key(self, key_code: int) -> None:
        if self.ui and self.e:
            self.ui.write(self.e.EV_KEY, key_code, 1)
            self.ui.write(self.e.EV_KEY, key_code, 0)
            self.ui.syn()
            
    def scroll(self, clicks: int) -> None:
        if self.ui and self.e:
            self.ui.write(self.e.EV_REL, self.e.REL_WHEEL, clicks)
            self.ui.syn()

    def hotkey(self, *key_codes: int) -> None:
        if self.ui and self.e:
            for k in key_codes:
                self.ui.write(self.e.EV_KEY, k, 1)
            for k in reversed(key_codes):
                self.ui.write(self.e.EV_KEY, k, 0)
            self.ui.syn()

uinput_manager = LinuxUInputManager()

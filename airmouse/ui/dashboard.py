import customtkinter as ctk
import threading
from airmouse.utils.logger import setup_logger

logger = setup_logger("ui")

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("AirMouse++ Dashboard")
        self.geometry("800x600")

        # configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="AirMouse++", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.btn_dashboard = ctk.CTkButton(self.sidebar_frame, text="Dashboard", command=self.show_dashboard)
        self.btn_dashboard.grid(row=1, column=0, padx=20, pady=10)
        
        self.btn_gestures = ctk.CTkButton(self.sidebar_frame, text="Gestures", command=self.show_gestures)
        self.btn_gestures.grid(row=2, column=0, padx=20, pady=10)
        
        self.btn_plugins = ctk.CTkButton(self.sidebar_frame, text="Plugins", command=self.show_plugins)
        self.btn_plugins.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 20))

        # Main content area
        self.main_frame = ctk.CTkFrame(self, corner_radius=10)
        self.main_frame.grid(row=0, column=1, rowspan=4, padx=20, pady=20, sticky="nsew")
        
        self.header_label = ctk.CTkLabel(self.main_frame, text="System Status: Ready", font=ctk.CTkFont(size=24, weight="bold"))
        self.header_label.pack(pady=20)
        
        self.start_engine_btn = ctk.CTkButton(self.main_frame, text="Start Engine", fg_color="green", hover_color="darkgreen", command=self.start_engine)
        self.start_engine_btn.pack(pady=20)
        
        self.stop_engine_btn = ctk.CTkButton(self.main_frame, text="Stop Engine", fg_color="red", hover_color="darkred", state="disabled")
        self.stop_engine_btn.pack(pady=10)

        # Default values
        self.appearance_mode_optionemenu.set("Dark")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def show_dashboard(self):
        self.header_label.configure(text="Dashboard")

    def show_gestures(self):
        self.header_label.configure(text="Gesture Mappings (Coming Soon)")

    def show_plugins(self):
        self.header_label.configure(text="Installed Plugins")

    def _run_engine_thread(self):
        from airmouse.core.opencv_camera import OpenCVCamera
        from airmouse.core.mediapipe_tracker import MediaPipeTracker
        from airmouse.core.rule_recognizer import RuleRecognizer
        from airmouse.core.config_mapper import ConfigMapper
        from airmouse.core.action_dispatcher import ActionDispatcher
        from airmouse.core.main_engine import MainEngine
        from airmouse.actions.mouse import MouseController
        from airmouse.actions.media import MediaController
        from airmouse.actions.system import SystemController
        from airmouse.actions.windows import WindowController
        
        camera = OpenCVCamera()
        tracker = MediaPipeTracker()
        recognizer = RuleRecognizer()
        mapper = ConfigMapper()
        dispatcher = ActionDispatcher()
        
        dispatcher.register_controller(MouseController())
        dispatcher.register_controller(MediaController())
        dispatcher.register_controller(SystemController())
        dispatcher.register_controller(WindowController())
        
        self.engine = MainEngine(camera, tracker, recognizer, mapper, dispatcher)
        self.engine.start()

    def start_engine(self):
        logger.info("GUI requested engine start.")
        self.start_engine_btn.configure(state="disabled")
        self.stop_engine_btn.configure(state="normal")
        self.header_label.configure(text="System Status: RUNNING", text_color="green")
        self.engine_thread = threading.Thread(target=self._run_engine_thread, daemon=True)
        self.engine_thread.start()

    def stop_engine(self):
        logger.info("GUI requested engine stop.")
        self.start_engine_btn.configure(state="normal")
        self.stop_engine_btn.configure(state="disabled")
        self.header_label.configure(text="System Status: Stopped", text_color="red")
        if hasattr(self, 'engine') and self.engine:
            self.engine.stop()

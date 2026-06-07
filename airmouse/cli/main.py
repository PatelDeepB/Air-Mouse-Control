import argparse
import sys
from airmouse.utils.logger import setup_logger

logger = setup_logger("cli")

def start_engine(args):
    """Starts the AirMouse++ background engine."""
    logger.info("Starting AirMouse++ Engine...")
    
    # Lazy import to avoid loading heavy CV modules for simple CLI commands
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
    
    # Initialize Core Components
    camera = OpenCVCamera()
    tracker = MediaPipeTracker()
    recognizer = RuleRecognizer()
    mapper = ConfigMapper()
    dispatcher = ActionDispatcher()
    
    # Register Controllers
    dispatcher.register_controller(MouseController())
    dispatcher.register_controller(MediaController())
    dispatcher.register_controller(SystemController())
    dispatcher.register_controller(WindowController())
    
    engine = MainEngine(camera, tracker, recognizer, mapper, dispatcher)
    
    try:
        engine.start()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received.")
    finally:
        engine.stop()

def start_gui(args):
    """Starts the AirMouse++ Desktop GUI Dashboard."""
    logger.info("Starting AirMouse++ Dashboard...")
    from airmouse.ui.dashboard import App
    app = App()
    app.mainloop()

def main():
    parser = argparse.ArgumentParser(description="AirMouse++ AI Gesture Control Framework")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: start
    start_parser = subparsers.add_parser("start", help="Start the gesture recognition engine in background")
    start_parser.set_defaults(func=start_engine)

    # Command: ui
    ui_parser = subparsers.add_parser("ui", help="Open the desktop dashboard")
    ui_parser.set_defaults(func=start_gui)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    args.func(args)

if __name__ == "__main__":
    main()

# Sample Plugin for AirMouse++
import webbrowser
from airmouse.core.plugin_manager import gesture

@gesture("open_browser")
def open_browser(**kwargs):
    """Opens the default web browser."""
    print("Executing open_browser plugin action...")
    webbrowser.open("https://github.com/PatelDeepB/Air-Mouse-Control")

@gesture("open_chatgpt")
def open_chatgpt(**kwargs):
    """Opens ChatGPT in the default browser."""
    print("Executing open_chatgpt plugin action...")
    webbrowser.open("https://chat.openai.com/")

<div align="center">
  <h1>🖱️ AirMouse++ : AI-Powered Hand Gesture Mouse Control</h1>

  <p><b>A cross-platform Python computer vision framework to control your mouse, keyboard, and operating system using nothing but your webcam and natural hand gestures.</b></p>

  [![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Platform: Windows | macOS | Linux](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)](#)
  
  *Keywords: `gesture-control`, `virtual-mouse`, `hand-tracking`, `mediapipe`, `opencv`, `python-automation`, `touchless-interface`, `ai-mouse`, `computer-vision`*
</div>

---

AirMouse++ is an open-source, cross-platform gesture control software that transforms any standard webcam into a touchless input device. Unlike a simple virtual mouse script, AirMouse++ is built as a robust automation framework where developers and power users can map AI hand tracking gestures to complex system actions. Built with Python, OpenCV, and Google MediaPipe.

## 📑 Table of Contents
- [💡 Top Use Cases](#-top-use-cases)
- [🚀 Features](#-features)
- [🛠️ Installation](#️-installation)
- [🎮 Usage](#-usage)
- [⚙️ Configuration](#️-configuration)
- [🔌 Writing Plugins](#-writing-plugins)
- [❓ FAQ](#-faq-frequently-asked-questions)

## 💡 Top Use Cases
- **Presentations:** Switch slides and point at the screen without holding a clicker.
- **Media Viewing:** Play, pause, or adjust volume from the couch using hand signs.
- **Accessibility:** Touchless computer navigation for users with limited mobility.
- **Clean Environments:** Browse recipes while cooking or read manuals while working with dirty hands.

## 🚀 Features

- **Cross-Platform:** Works on Windows, macOS, and Linux.
- **Core OS Control:** Move your mouse, drag-and-drop, right-click, double-click, and scroll using just your hands.
- **Zero-Jitter UX:** Utilizes a highly tuned One Euro Filter on absolute coordinates and implements Click Stabilization (freezing the cursor when clicking) to eliminate misclicks.
- **Machine Learning Trainer:** Ships with a built-in CLI trainer (`airmouse train`) to record your own hand shape and train a custom K-Nearest Neighbors ML classifier for 100% accurate, personalized gesture recognition.
- **Plugin System:** Extend the framework by dropping Python scripts into the `plugins/` directory and decorating functions with `@gesture("action_name")`.
- **Beautiful UI:** Comes with a CLI (`airmouse`) and a dark-themed CustomTkinter Desktop Dashboard.

## 🛠️ Installation

**1. Clone the repository:**
```bash
git clone https://github.com/PatelDeepB/Air-Mouse-Control.git
cd Air-Mouse-Control
```

### Ubuntu / Linux Setup
On Ubuntu, you will need to install system-level dependencies before `pip install` works correctly:
```bash
sudo apt-get update
sudo apt-get install python3-tk python3-dev libgl1-mesa-glx libglib2.0-0
```
> [!IMPORTANT]
> If you are running Ubuntu 22.04+ with the **Wayland** display server, AirMouse++ natively supports Wayland by injecting input directly into the Linux kernel using `evdev`. 
> However, for security reasons, this means **you must run the application with sudo:**
> `sudo airmouse start`

**2. Install dependencies:**
```bash
pip install -e .
```

## 🎮 Usage

### Start via CLI
You can start the background gesture engine directly from the command line:
```bash
airmouse start
```

### Start via Dashboard UI
To launch the graphical control panel:
```bash
airmouse ui
```

## ⚙️ Configuration
AirMouse++ uses a `config.yaml` file to map recognized gestures to actual OS actions. Create a `config.yaml` in the project root:

```yaml
camera:
  comfort_margin_x: 0.2  # Increase to 0.3 or 0.4 to reduce horizontal arm movement
  comfort_margin_y: 0.2  # Increase to reduce vertical arm movement

gestures:
  point: "move" # Index finger to move
  pinch: "left_click_drag" # Hold pinch to drag
  shaka: "right_click" # Thumb and pinky extended
  double_pinch: "double_click"
  thumb_up: "scroll_up" # Thumbs up to scroll up
  thumb_down: "scroll_down" # Thumbs down to scroll down
```

## 🔌 Writing Plugins
Creating a plugin is extremely simple. Just create a file in the `plugins/` folder (e.g., `my_plugin.py`):

```python
from airmouse.core.plugin_manager import gesture
import webbrowser

@gesture("open_browser")
def open_browser(**kwargs):
    webbrowser.open("https://github.com")
```
Then map a gesture to `open_browser` in your `config.yaml`.

## ❓ FAQ (Frequently Asked Questions)

**Can I control my mouse with a webcam?**  
Yes! AirMouse++ uses your standard webcam to track your hand joints in 3D space, translating your finger movements into precise mouse coordinates.

**What is the best Python virtual mouse?**  
AirMouse++ is designed to be the most robust Python virtual mouse. It uses a One Euro Filter to eliminate cursor shaking and Click Stabilization to ensure you don't accidentally move the mouse while clicking.

**Does it work on Mac and Linux?**  
Yes, it is fully cross-platform. It uses `pynput` and `pyautogui` which support Windows, macOS, and X11 Linux out of the box. For modern Wayland Linux environments (like Ubuntu 22.04+), it uses native kernel-level `evdev` injection (requires `sudo`).

## 🤝 Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 🧪 Experimental: Custom ML Gestures
We are currently actively developing the `airmouse train` CLI command. This feature will soon allow users to calculate joint angles and train highly robust custom ML models for personalized gestures. Stay tuned!

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

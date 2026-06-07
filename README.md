# AirMouse++

> Control your entire computer using nothing but your webcam and natural hand gestures.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

AirMouse++ is an open-source, cross-platform gesture control framework that transforms any webcam into a touchless input device. Unlike a simple virtual mouse, AirMouse++ is designed as a modular automation framework where users and developers can map custom hand gestures to any computer action.

## 🚀 Features

- **Cross-Platform:** Works on Windows, macOS, and Linux.
- **Core OS Control:** Move your mouse, click, scroll, switch windows, adjust volume, and control media playback using just your hands.
- **Rule-Based & ML Recognition:** Ships with highly optimized heuristics for common gestures (pinch, fist, peace sign) and includes a machine learning trainer (KNN) to record and classify custom gestures.
- **Plugin System:** Extend the framework by dropping Python scripts into the `plugins/` directory and decorating functions with `@gesture("action_name")`.
- **Beautiful UI:** Comes with a CLI (`airmouse`) and a dark-themed CustomTkinter Desktop Dashboard.

## 🛠️ Installation

**1. Clone the repository:**
```bash
git clone https://github.com/PatelDeepB/Air-Mouse-Control.git
cd Air-Mouse-Control
```

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
gestures:
  pinch: "left_click"
  fist: "play_pause"
  peace: "switch_next"
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

## 🤝 Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**. Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📄 License
Distributed under the MIT License. See `LICENSE` for more information.

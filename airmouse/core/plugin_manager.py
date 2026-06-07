import os
import importlib.util
from typing import Callable, Dict, Any
from pathlib import Path
from airmouse.utils.logger import setup_logger

logger = setup_logger("plugin_manager")

# Global registry for plugin actions
_PLUGIN_REGISTRY: Dict[str, Callable] = {}

def gesture(action_name: str):
    """
    Decorator to register a function as a custom action for a specific gesture.
    
    Args:
        action_name: The name of the action/gesture to bind to.
    """
    def decorator(func: Callable):
        _PLUGIN_REGISTRY[action_name] = func
        return func
    return decorator

class PluginManager:
    """Manages dynamic loading of third-party plugins."""

    def __init__(self, plugins_dir: str = "plugins"):
        self.plugins_dir = Path(plugins_dir)

    def load_plugins(self) -> None:
        """Dynamically imports all python files in the plugins directory."""
        if not self.plugins_dir.exists():
            self.plugins_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created plugins directory at {self.plugins_dir}")
            return

        for plugin_file in self.plugins_dir.glob("*.py"):
            if plugin_file.name == "__init__.py":
                continue
                
            module_name = plugin_file.stem
            try:
                spec = importlib.util.spec_from_file_location(module_name, plugin_file)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    logger.info(f"Loaded plugin module: {module_name}")
            except Exception as e:
                logger.error(f"Failed to load plugin {module_name}: {e}")

    def register_to_dispatcher(self, dispatcher: Any) -> None:
        """Registers all loaded plugin actions to the ActionDispatcher."""
        for action_name, func in _PLUGIN_REGISTRY.items():
            # Inject directly into dispatcher registry
            dispatcher.action_registry[action_name] = func
            logger.info(f"Registered plugin action to dispatcher: {action_name}")

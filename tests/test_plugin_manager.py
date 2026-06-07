import os
import shutil
from pathlib import Path
from airmouse.core.plugin_manager import PluginManager, _PLUGIN_REGISTRY, gesture
from airmouse.core.action_dispatcher import ActionDispatcher

def test_plugin_registration():
    # Clear registry for testing
    _PLUGIN_REGISTRY.clear()

    @gesture("test_action")
    def my_plugin_action(**kwargs):
        pass

    assert "test_action" in _PLUGIN_REGISTRY
    assert _PLUGIN_REGISTRY["test_action"] == my_plugin_action

def test_plugin_loading_and_dispatching(tmp_path):
    _PLUGIN_REGISTRY.clear()
    
    # Create a dummy plugin file in tmp_path
    plugin_dir = tmp_path / "plugins"
    plugin_dir.mkdir()
    plugin_file = plugin_dir / "my_plugin.py"
    
    plugin_code = '''
from airmouse.core.plugin_manager import gesture

@gesture("dynamic_action")
def dynamic(**kwargs):
    kwargs["state"]["called"] = True
'''
    plugin_file.write_text(plugin_code)

    manager = PluginManager(plugins_dir=str(plugin_dir))
    manager.load_plugins()

    assert "dynamic_action" in _PLUGIN_REGISTRY

    dispatcher = ActionDispatcher()
    manager.register_to_dispatcher(dispatcher)

    assert "dynamic_action" in dispatcher.action_registry

    # Test execution
    state = {"called": False}
    dispatcher.dispatch("dynamic_action", state=state)
    assert state["called"] is True

from unittest.mock import patch, MagicMock
from airmouse.core.config_mapper import ConfigMapper
from airmouse.core.action_dispatcher import ActionDispatcher

@patch("airmouse.core.config_mapper.load_settings")
def test_config_mapper(mock_load_settings):
    mock_settings = MagicMock()
    mock_settings.gestures = {"pinch": "left_click", "peace": "screenshot"}
    mock_load_settings.return_value = mock_settings

    mapper = ConfigMapper("dummy_config.yaml")
    
    assert mapper.get_action("pinch") == "left_click"
    assert mapper.get_action("peace") == "screenshot"
    assert mapper.get_action("unknown_gesture") is None

def test_action_dispatcher():
    dispatcher = ActionDispatcher()
    
    class DummyController:
        def __init__(self):
            self.clicked = False
            self.coords = None
            
        def left_click(self):
            self.clicked = True
            
        def move(self, target_x: float, target_y: float):
            self.coords = (target_x, target_y)
            
        def _private_method(self):
            pass

    controller = DummyController()
    dispatcher.register_controller(controller)
    
    # Check registration
    assert "left_click" in dispatcher.action_registry
    assert "move" in dispatcher.action_registry
    assert "_private_method" not in dispatcher.action_registry
    
    # Test dispatching simple action
    success = dispatcher.dispatch("left_click")
    assert success is True
    assert controller.clicked is True
    
    # Test dispatching action with kwargs
    success = dispatcher.dispatch("move", target_x=100.5, target_y=200.5)
    assert success is True
    assert controller.coords == (100.5, 200.5)
    
    # Test dispatching unknown action
    success = dispatcher.dispatch("unknown_action")
    assert success is False

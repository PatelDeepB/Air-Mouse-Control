from typing import Any, Dict, List
from airmouse.core.dispatcher import BaseDispatcher
from airmouse.utils.logger import setup_logger

logger = setup_logger("action_dispatcher")

class ActionDispatcher(BaseDispatcher):
    """Dispatches actions to registered controllers."""

    def __init__(self):
        self.controllers: List[Any] = []
        # A registry mapping action names (like 'play_pause', 'left_click') 
        # to the actual controller methods.
        self.action_registry: Dict[str, callable] = {}

    def register_controller(self, controller: Any) -> None:
        self.controllers.append(controller)
        # Automatically register public methods of the controller
        for attr_name in dir(controller):
            if not attr_name.startswith('_'):
                attr_value = getattr(controller, attr_name)
                if callable(attr_value):
                    self.action_registry[attr_name] = attr_value
                    logger.info(f"Registered action: {attr_name}")

    def dispatch(self, action_name: str, **kwargs) -> bool:
        if action_name in self.action_registry:
            func = self.action_registry[action_name]
            try:
                func(**kwargs)
                return True
            except Exception as e:
                logger.error(f"Error executing action {action_name}: {e}")
                return False
        else:
            logger.warning(f"Action not found: {action_name}")
            return False

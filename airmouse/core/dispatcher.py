from abc import ABC, abstractmethod
from typing import Any

class BaseDispatcher(ABC):
    """Abstract base class for dispatching actions to controllers."""

    @abstractmethod
    def dispatch(self, action_name: str, **kwargs) -> bool:
        """
        Executes the given action.

        Args:
            action_name: The name of the action to execute.
            **kwargs: Additional parameters for the action (e.g., coordinates for mouse move).

        Returns:
            True if the action was successfully dispatched and handled, False otherwise.
        """
        pass

    @abstractmethod
    def register_controller(self, controller: Any) -> None:
        """
        Registers a controller (e.g., MouseController, MediaController) to handle actions.
        """
        pass

import os

from flashy.models.user.definition import USER_DEFINITIONS
from flashy.models.parameters.container import ParameterContainer

from typing import Any, override

class UserConfig(ParameterContainer):
    """
    Dataclass for the user's configuration.
    
    :inherits: ParameterContainer
    """
    DEFINITIONS = USER_DEFINITIONS
    """
    Parameter definitions for user (See :py:data:`~flashy.models.user.definition.USER_DEFINITIONS`).
    
    :meta hide-value:
    """
    
    @override
    def set_value(self, key: str, raw_value: Any):
        super().set_value(key, raw_value)
        
        # Recompute only affected derived values
        try:
            if key == "name_of_shoot":
                self._recompute("name_of_shoot")
                increment_name = self._recompute("increment_name")
                path_of_shoot = self._recompute("path_of_shoot")
                
                # Validation
                self.values["increment_name"] = increment_name
                self.values["path_of_shoot"] = path_of_shoot
            elif key in {"project_path", "increment"}:
                increment_name = self._recompute("increment_name")
                path_of_shoot = self._recompute("path_of_shoot")
                
                # Validation
                self.values["increment_name"] = increment_name
                self.values["path_of_shoot"] = path_of_shoot
        except Exception:
            # Rollback: Derive state from current valid config
            self._rollback_values()
            raise
    
    def _recompute(self, key: str):
        if key == "name_of_shoot":
            self.values["increment"] = 1
        elif key == "increment_name":
            increment_name = (
                f"{self.values['name_of_shoot']}_"
                f"{self.values['increment']}"
            )
            return increment_name
        elif key == "path_of_shoot":
            increment_name = (
                f"{self.values['name_of_shoot']}_"
                f"{self.values['increment']}"
            )
            path = os.path.join(self.values["project_path"], increment_name)
            
            # Validation
            if os.path.exists(path):
                raise FileExistsError(
                    f"'{path}' already exists. Refusing update."
                )
            
            return path
    
    def _rollback_values(self): 
        self.values["increment_name"] = (
            f"{self.values['name_of_shoot']}_{self.values['increment']}"
        ) 
        self.values["path_of_shoot"] = os.path.join(
            self.values["project_path"], 
            self.values["increment_name"]
        )
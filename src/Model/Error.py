from caen_felib import error
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.Controller.Controller import Controller    

class Error:
    def __init__(self, controller:"Controller") -> None:
         self.controller = controller
         self.send_feedback = controller.view_controller.send_feedback
         
    def handle_CAEN_exceptions(self, func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except error.Error as ex:
                # -6: Command error
                if ex.code.value == error.ErrorCode.COMMAND_ERROR:
                    self.controller.change_states()
                    self.send_feedback(f"Error code {ex.code.value} (COMMAND_ERROR): Couldn't find a digitizer to connect to!")
                
                # Not something defined
                else:
                    self.controller.change_states()
                    self.send_feedback(f"Error code {ex.code.value}: Unexpected! Raising error (see terminal)")
                    raise ex
        return wrapper
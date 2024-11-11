from typing import Any, Dict
from Controller.ModelController import ModelController
from Controller.ViewController import ViewController
from Model.Error import Error

# This class contains all the different settings of the program and
# is used as a link between the models and the views
class Controller():
    def __init__(self, view_controller:ViewController, model_controller:ModelController) -> None:
        self.view_controller = view_controller
        self.model_controller = model_controller
        self.error_handling = Error(self)
        
        # Settings initialization
        self.RECORD_LENGHT:str = '0'
        self.PRE_TRIGGER:str = '0'
        
        # User can choose how the area is calculated
        self.AREA_CALCULATION_METHOD = 'trap' # ["naif", "trap"]
        # User can choose how the pulse is leveled
        self.LEVELING_METHOD = 'dynamic-median' # ["median", "dynamic-mean", "dynamic-median"]
        
        # Bool that determines the state of the program
        self.isCONNECTING_TO_DIG:bool = False
        self.isTAKING_DATA:bool = False
        self.isCHANGING_SETTINGS:bool = False
        self.isGETTING_BASIC_INFO: bool = False
        self.isRECORDING:bool = False
        
        self.hasDIGITIZERCONNECTED: bool = False
    
    # Getting information from the models
    def get_data_analyser(self):
        return self.model_controller.get_data_analyser()
    def get_digitizer(self):
        return self.model_controller.get_digitizer()
        
    # Determines if the digitizer can be used
    def can_use_dig(self):
        if self.isCONNECTING_TO_DIG or self.isCHANGING_SETTINGS \
        or self.isTAKING_DATA or self.isGETTING_BASIC_INFO \
        or self.isRECORDING:
            return False
        return True
    
    # Used by exception handeling
    def change_states(self):
        self.isCONNECTING_TO_DIG:bool = False
        self.isTAKING_DATA:bool = False
        self.isCHANGING_SETTINGS:bool = False
        self.isGETTING_BASIC_INFO: bool = False
        self.isRECORDING = False
    
    # From models to views
    def send_feedback(self, message:str):
        self.view_controller.send_feedback(message)
    # TODO: Change these so its like send_feedback    
    def change_aqc_panel_message(self):
        self.view_controller.bypass.data_aqc_panel.status_text
    def dispatch_data(self, data:Dict[str, Any]):
        self.view_controller.bypass.dig_info_panel.dispatch_data(data)
    def change_aqc_panel_status(self, message:str):
        self.view_controller.bypass.data_aqc_panel.change_aqc_panel_status(message)
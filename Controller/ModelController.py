from Model.Digitizer import Digitizer
from Model.DataAnalyser import DataAnalyser

from typing import TYPE_CHECKING, Any, Dict
if TYPE_CHECKING:
    from Controller.Controller import Controller

# This class is for taking care of the communication between the different models
# For example, the SaveFile needs to access the DataAnalyser
# It's also a link between the controller and the models for updating the views
class ModelController():
    def __init__(self) -> None:
        pass
    
    def set_up(self, controller: "Controller"):
        self.controller = controller
        self.data_analyser = DataAnalyser(self) 
        self.digitizer = Digitizer(self)
    
    # Getting information from the data analyser
    def get_data_analyser(self):
        return self.data_analyser
    def get_digitizer(self):
        return self.digitizer
        
    # The following functions are for communicating with the views
    def get_rcd_len(self):
        return self.controller.RECORD_LENGHT
    def get_AREA_CALCULATION_METHOD(self):
        return self.controller.AREA_CALCULATION_METHOD
    def get_LEVELING_METHOD(self):
        return self.controller.LEVELING_METHOD
    
    def send_feedback(self, message:str):
        self.controller.send_feedback(message)
    def dispatch_data(self, data:Dict[str, Any]):
        self.controller.dispatch_data(data)
    def change_aqc_panel_status(self, message:str):
        self.controller.change_aqc_panel_status(message)
    # TODO: Make this like the others
    def update_pulse_graph(self):
        self.controller.view_controller.graph_showcase.update_pulse_graph()
    def update_area_graph(self):
        self.controller.view_controller.graph_showcase.update_area_graph()
    def update_list(self):
        self.controller.view_controller.graph_showcase.update_list()
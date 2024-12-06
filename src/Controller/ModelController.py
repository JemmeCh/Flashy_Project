from src.Model.Digitizer import Digitizer
from src.Model.DataAnalyser import DataAnalyser

from typing import TYPE_CHECKING, Any, Dict
if TYPE_CHECKING:
    from src.Controller.Controller import Controller
    from src.View.GraphShowcase import GraphShowcase

# This class is for taking care of the communication between the different models
# It's also a link between the controller and the models for updating the views
class ModelController():
    def __init__(self) -> None:
        pass
    
    def set_up(self, controller: "Controller"):
        self.controller = controller
        self.data_analyser = DataAnalyser(self) 
        self.ch0_analyser = DataAnalyser(self)
        self.ch1_analyser = DataAnalyser(self)
        self.raw_analyser = DataAnalyser(self)
        self.digitizer = Digitizer(self)
    
    # Getting information from the data analyser
    def get_data_analyser(self):
        return self.data_analyser
    def get_ch0_analyser(self):
        return self.ch0_analyser
    def get_ch1_analyser(self):
        return self.ch1_analyser
    def get_raw_analyser(self):
        return self.raw_analyser
    def get_digitizer(self):
        return self.digitizer
        
    # The following functions are for communicating with the views
    def get_rcd_len(self):
        return self.controller.get_RECORD_LENGHT()
    def get_AREA_CALCULATION_METHOD(self):
        return self.controller.get_AREA_CALCULATION_METHOD()
    def get_LEVELING_METHOD(self):
        return self.controller.get_LEVELING_METHOD()
    
    def send_feedback(self, message:str):
        self.controller.send_feedback(message)
    def dispatch_data(self, data:Dict[str, Any]):
        self.controller.dispatch_data(data)
    def change_aqc_panel_status(self, message:str):
        self.controller.change_aqc_panel_status(message)
    def update_pulse_graph(self):
        self.controller.view_controller.graph_showcase.update_pulse_graph()
    def update_area_graph(self):
        self.controller.view_controller.graph_showcase.update_area_graph()
    def update_list(self):
        self.controller.view_controller.graph_showcase.update_list()
    
    """Functions for updating the graph showcases"""    
    def analyse_data(self, graph_showcase:"GraphShowcase", analyser:DataAnalyser, data):
        analyser.analyse_data(graph_showcase, data)
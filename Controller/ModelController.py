from Model.DataAnalyser import DataAnalyser

from typing import TYPE_CHECKING
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
    
    # Getting information from the data analyser
    def get_data_analyser(self):
        return self.data_analyser
        
    # The following functions are for communicating with the views
    def send_feedback(self, message:str): #TODO
        self.controller
    def get_rcd_len(self):
        return self.controller.RECORD_LENGHT
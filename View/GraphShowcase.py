from tkinter import ttk

from View.Graphs.AreaGraph import AreaGraph
from View.Graphs.PulseGraph import PulseGraph
from View.ListOfResults import ListOfResults

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Controller.ViewController import ViewController

class GraphShowcase(ttk.Frame):
    def __init__(self, parent, view_controller:"ViewController") -> None:
        super().__init__(parent, padding=(10,10), relief="raised")
        
        # Used to modify/get other parts of the program
        self.view_controller = view_controller
        
        # Pulses' forms graph
        self.pulse_graph = PulseGraph(self, "Temps (µs)", "Voltage (V)", 
                                          True, gridrow=0, gridcolumn=0)
        
        # Area per pulse graph
        self.area_graph = AreaGraph(self, "Nombre de pulse", "Aires (nC)", 
                                          True, gridrow=2, gridcolumn=0)
        
        # List of results spanning both rows
        self.list = ListOfResults(self)
        self.list.grid(row=0,column=1, rowspan=4, sticky="nsew")
        
        # Configure row/column weight for grid responsiveness
        self.grid_rowconfigure(0, weight=1)  # First graph row
        self.grid_rowconfigure(2, weight=1)  # Second graph row
        self.grid_columnconfigure(0, weight=1)  # Left column (both graphs)
        self.grid_columnconfigure(1, weight=1)  # Right column (spanning list)
        
    def update_pulse_graph(self):
        self.pulse_graph.update_graph()
    def update_area_graph(self):
        self.area_graph.update_graph()
    def update_list(self): 
        self.list.update_list()
        
    def fetch_pulse_info(self):
        return self.view_controller.data_analyser.get_pulse_info()
    def fetch_t_axis(self):
        return self.view_controller.data_analyser.get_t_axis()
    def fetch_area_under_curve(self):
        return self.view_controller.data_analyser.get_area_under_curve()
    def fetch_nbr_of_pulse(self):
        return self.view_controller.data_analyser.get_nbr_of_pulse()
    def fetch_data_list(self):
        return self.view_controller.data_analyser.get_data_list()

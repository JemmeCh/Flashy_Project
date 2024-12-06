from tkinter import ttk

from src.View.Graphs.AreaGraph import AreaGraph
from src.View.Graphs.PulseGraph import PulseGraph
from src.View.ListOfResults import ListOfResults

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.Controller.ViewController import ViewController
    from src.Model.DataAnalyser import DataAnalyser

class GraphShowcase(ttk.Frame):
    def __init__(self, parent, view_controller:"ViewController",
                 data_analyser:"DataAnalyser") -> None:
        super().__init__(parent, padding=(10,10), relief="raised")
        
        # Used to modify/get other parts of the program
        self.view_controller = view_controller
        self.data_analyser = data_analyser
        
        # Pulses' forms graph
        self.pulse_graph = PulseGraph(self, "Temps (µs)", "Voltage (V)", 
                                          True, self.data_analyser, gridrow=0, gridcolumn=0)
        
        # Area per pulse graph
        self.area_graph = AreaGraph(self, "Nombre de pulse", "Aires (nC)", 
                                          True, self.data_analyser, gridrow=2, gridcolumn=0)
        
        # List of results spanning both rows
        self.list = ListOfResults(self, self.data_analyser)
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

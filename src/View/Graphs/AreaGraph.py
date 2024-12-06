import numpy as np

from src.View.Graphs.Graph import Graph

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.View.GraphShowcase import GraphShowcase
    from src.Model.DataAnalyser import DataAnalyser

class AreaGraph(Graph):
    def __init__(self, parent:"GraphShowcase", x_label:str, y_label:str, 
                 toolbar:bool, analyser:"DataAnalyser", gridrow:int, gridcolumn:int):
        self.showcase = parent
        self.analyser = analyser
        self.x_label = x_label
        self.y_label = y_label
        self.toolbar_bool = toolbar
        self.gridrow = gridrow
        self.gridcolumn = gridcolumn
        super().create_plot_canvas()
        
        # Place graph
        if self.toolbar_bool:
            self.toolbar.grid(row=self.gridrow + 1, column=self.gridcolumn, sticky="n")
        self.canvas.get_tk_widget().grid(row=self.gridrow, column=self.gridcolumn, sticky="nsew")
        
    def update_graph(self):
        # Clear the old canvas
        self.create_plot_canvas()
        if self.toolbar_bool:
            self.toolbar.grid(row=self.gridrow + 1, column=self.gridcolumn, sticky="n")
        self.canvas.get_tk_widget().grid(row=self.gridrow, column=self.gridcolumn, sticky="nsew")
        
        # Get the new values of x and y
        self.x = self.analyser.get_nbr_of_pulse() #showcase.fetch_nbr_of_pulse()
        self.y = self.analyser.get_area_under_curve() #showcase.fetch_area_under_curve()
        self.x = np.arange(self.x) + 1
        self.y = np.array(self.y)
        
        # Update plot
        self.ax.plot(self.x, self.y,'ro',linestyle='dashed',markersize=10)
        # Put labels
        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)

        self.ax.autoscale_view()
        
        self.canvas.draw()

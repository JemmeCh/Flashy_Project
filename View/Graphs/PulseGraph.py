import numpy as np

from View.Graphs.Graph import Graph

class PulseGraph(Graph):
    def __init__(self, parent, x_label:str, y_label:str, 
                 toolbar:bool, gridrow:int, gridcolumn:int):
        self.showcase = parent
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
        self.x = self.showcase.fetch_t_axis()
        self.y = self.showcase.fetch_pulse_info()
        self.x = np.array(self.x)
        self.y = np.array(self.y)

        # Update plot
        for pulse in self.y:
            self.ax.plot(self.x, pulse)
        # Put labels
        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)
        
        self.ax.autoscale_view()
        
        self.canvas.draw()
 
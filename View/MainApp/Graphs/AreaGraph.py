import numpy as np

from View.MainApp.Graphs.Graph import Graph

class AreaGraph(Graph):
    def __init__(self, parent, x_label:str, y_label:str, 
                 toolbar:bool):
        self.showcase = parent
        self.x_label = x_label
        self.y_label = y_label
        self.toolbar_bool = toolbar
        super().create_plot_canvas()
        
    def update_graph(self):
        # Clear the old canvas
        self.create_plot_canvas()
        if self.toolbar_bool:
            self.toolbar.grid(row=3, column=0, sticky="n")
        self.canvas.get_tk_widget().grid(row=2, column=0, sticky="nsew")
        
        # Get the new values of x and y
        self.x = self.showcase.fetch_nbr_of_pulse()
        self.y = self.showcase.fetch_area_under_curve()
        self.x = np.arange(self.x)
        self.y = np.array(self.y)
        
        # Update plot
        self.ax.plot(self.x, self.y,'ro',linestyle='dashed',markersize=10)
        # Put labels
        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)

        self.ax.autoscale_view()
        
        self.canvas.draw()

import numpy as np

from View.MainApp.Graphs.Graph import Graph

class AreaGraph(Graph):
    def __init__(self, parent, x_label:str, y_label:str, 
                 toolbar:bool):
        super().__init__(parent, x_label, y_label, toolbar)
        self.showcase = parent
        self.x = self.showcase.fetch_nbr_of_pulse()
        self.y = self.showcase.fetch_area_under_curve()
        
    def update_graph(self):
        # Clear the old canvas
        self.create_plot_canvas(self.showcase,self.x_label,self.y_label)
        self.canvas.get_tk_widget().grid(row=2, column=0, sticky="nsew")

        
        # Get the new values of x and y
        self.x = self.showcase.fetch_nbr_of_pulse()
        self.y = self.showcase.fetch_area_under_curve()
        self.x = np.arange(self.x)
        self.y = np.array(self.y)
        
        # Update plot
        self.ax.clear()
        self.ax.plot(self.x, self.y,'ro',linestyle='dashed',markersize=10)

        self.ax.autoscale_view()
        
        self.canvas.draw()

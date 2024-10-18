import numpy as np

from View.MainApp.Graphs.Graph import Graph

class PulseGraph(Graph):
    def __init__(self, parent, x_label:str, y_label:str, 
                 toolbar:bool):
        super().__init__(parent, x_label, y_label, toolbar)
        """         
        self.x = self.showcase.fetch_t_axis()
        self.y = self.showcase.fetch_pulse_info() """
        
    def update_graph(self):
        # Clear the old canvas
        self.create_plot_canvas(self.showcase,self.x_label,self.y_label)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        
        # Get the new values of x and y
        self.x = self.showcase.fetch_t_axis()
        self.y = self.showcase.fetch_pulse_info()
        self.x = np.array(self.x)
        self.y = np.array(self.y)

        # Update plot
        self.ax.clear()
        for pulse in self.y:
            self.ax.plot(self.x, pulse)

        self.ax.autoscale_view()
        
        self.canvas.draw()
 
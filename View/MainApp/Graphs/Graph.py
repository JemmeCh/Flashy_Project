import numpy as np
import matplotlib
from matplotlib import pyplot as plt
matplotlib.use('TkAgg')
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler

class Graph:
    def __init__(self, parent, x_label:str, y_label:str, 
                 toolbar:bool) -> None:
        self.create_plot_canvas(parent,x_label,y_label)
        
        self.showcase = parent
        self.x_label = x_label
        self.y_label = y_label
        self.toolbar_bool = toolbar
        
        #self.canvas.draw()
        # Plot holder
        self.x = np.arange(25)
        self.y = np.arange(25)
        self.line, = self.ax.plot(self.x, self.y)
        #self.ax.plot(self.x, self.y)
        
        # Tool bar
        if toolbar:
            self.toolbar = NavigationToolbar2Tk(self.canvas, parent, pack_toolbar=False)
            self.toolbar.update()
            self.toolbar.grid(row=1, column=0, sticky="n")
        
        # Some test
        #self.canvas.mpl_connect("key_press_event", self.on_key_press)
        self.canvas.mpl_connect("key_press_event", key_press_handler) # type: ignore
    
    def create_plot_canvas(self, parent, x_label:str, y_label:str,):
        # Create a new figure and axis
        self.fig = Figure(figsize=(6,5))
        self.ax = self.fig.add_subplot()
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.fig.tight_layout()
        self.ax.set_autoscale_on(True)
        self.ax.set_adjustable('datalim')
        self.ax.autoscale(True, 'both')
        
        # Creating canvas where plot is drawn
        if hasattr(self, 'canvas'):  # If canvas already exists, destroy it
            self.canvas.get_tk_widget().destroy()

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        

    # The other Graph classes must change this
    def update_graph(self):
        pass  
    
    def on_key_press(self, event):
        print(f"you pressed {event.key}")
 
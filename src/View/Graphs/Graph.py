import numpy as np
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib import backend_bases

from src.View.Style import LIGHT_GRAY, DARK_GRAY

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.View.GraphShowcase import GraphShowcase

# Modifiying the toolbar
backend_bases.NavigationToolbar2.toolitems = (
    ('Home', 'Reset original view', 'home', 'home'),
    ('Back', 'Back to  previous view', 'back', 'back'),
    ('Forward', 'Forward to next view', 'forward', 'forward'),
    (None, None, None, None),
    ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
    ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
    #('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'),
    (None, None, None, None),
    ('Save', 'Save the figure', 'filesave', 'save_figure'),
)

class Graph:
    def __init__(self, parent:"GraphShowcase", x_label:str, y_label:str, 
                 toolbar:bool) -> None:
        self.create_plot_canvas()
        self.showcase = parent
        self.x_label = x_label
        self.y_label = y_label
        self.toolbar_bool = toolbar
    
    def create_plot_canvas(self):
        # Create a new figure and axis
        self.fig = Figure(figsize=(3,3))
        self.ax = self.fig.add_subplot()

        # Creating canvas where plot is drawn
        if hasattr(self, 'canvas'):  # If canvas already exists, destroy it
            self.canvas.get_tk_widget().destroy()
            # Create a new figure and axis
            self.fig = Figure(figsize=(3,3))
            self.ax = self.fig.add_subplot()
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.showcase)
        
        # Tool bar
        if self.toolbar_bool:
            if hasattr(self, 'toolbar'):  # If toolbar already exists, destroy it
                self.toolbar.destroy()
            self.ax.format_coord = lambda x,y: "" 
            self.toolbar = NavigationToolbar2Tk(self.canvas, self.showcase, pack_toolbar=False)
            self.toolbar.update()
            #self.toolbar.grid(row=1, column=0, sticky="n")
        
        # Making the layout tight and removing white space
        self.fig.tight_layout()
        self.fig.subplots_adjust(top=0.95, right=0.96, bottom=0.15, left=0.1)
        
        # Coloring the canvas
        self.ax.set_facecolor(LIGHT_GRAY)
        self.fig.set_facecolor(LIGHT_GRAY)
        self.fig.set_edgecolor(DARK_GRAY)
        

    # The other Graph classes must change this
    def update_graph(self):
        pass  
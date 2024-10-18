import numpy as np
import tkinter as tk
from tkinter import ttk

class ListOfResults(ttk.Treeview):
    def __init__(self, parent):
        super().__init__(parent, columns=("Pulse", "Aire sous la courbe", "Dose"), 
                 show="headings")
        self.showcase = parent
        
        self.column("Pulse", anchor="center",width=15, stretch=True)
        self.column("Aire sous la courbe", anchor="center",width=25, stretch=True)
        self.column("Dose", anchor="center",width=25, stretch=True)
        
        self.heading("Pulse", text="Pulse")
        self.heading("Aire sous la courbe", text="Aire sous la courbe")
        self.heading("Dose", text="Dose")
        
        self.grid(row=0,column=0,sticky="nsew")
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1) 
        
    def create_heading(self, parent, text, width) -> tk.Label:
        label = tk.Label(parent, text=text, wraplength=width, justify="center")
        label.grid(sticky="ew")
        return label
        
    def update_list(self):
        # Delete old results
        self.delete(*self.get_children())
        
        # Fetch the new data from DataAnalyser
        self.areas = self.showcase.fetch_area_under_curve() 
        self.nbr_of_pulse = self.showcase.fetch_nbr_of_pulse()
        self.doses = np.arange(self.nbr_of_pulse) # TODO: Calculate this
        
        # Packing data to be read by the List
        # Format: [[1,area1,dose1], [2,area2,dose2], ..., 
        # [self.nbr_of_pulse,area(self.nbr_of_pulse),dose(self.nbr_of_pulse)]]
        self.data = [[i + 1, area, dose] for i, (area, dose) in 
                     enumerate(zip(self.areas, self.doses))]
                
        for item in self.data:
            self.insert("", tk.END, values=item)
 
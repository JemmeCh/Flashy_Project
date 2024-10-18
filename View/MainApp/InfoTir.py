from tkinter import ttk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Controller.ViewController import ViewController

class InfoTir(ttk.LabelFrame):
    def __init__(self, view_controller:"ViewController"):
        super().__init__(view_controller, text="Information sur le tir", padding=(10,10), relief="raised")

        # --- Record lenght ---
        self.record_lenght = SettingEntryFrame(self, "Record Lenght", "15 000")
        self.record_lenght.grid(row=0, column=0, sticky="nswe")
        view_controller.set_rcd_len(15000)
        
        # --- Pre trigger ---
        self.pre_trigger = SettingEntryFrame(self, "Pre Trigger", "5 000")
        self.pre_trigger.grid(row=1, column=0, sticky="nswe")
        view_controller.set_pre_trigger(5000)
        
        self.grid_columnconfigure(0, weight=1) # Allow column to expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

# Used for creating a parameter
# TODO: Make it so you can change those values       
class SettingEntryFrame(ttk.Frame):
    def __init__(self, parent:InfoTir, label:str, init_val:str):
        super().__init__(parent)
        
        label_width = 15 # Align the labels
        
        self.label_recLen = ttk.Label(self, text=label, width=label_width)
        self.label_recLen.grid(row=0, column=0, sticky="w",padx=5, pady=5)
        
        self.record_lenght = ttk.Entry(self)
        self.record_lenght.insert(0, init_val)
        self.record_lenght.config(state="readonly") 
        self.record_lenght.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        self.unit_recLen = ttk.Label(self, text="ns")
        self.unit_recLen.grid(row=0, column=2, sticky="w",padx=5, pady=5)

        self.grid_columnconfigure(0, weight=0) # Fixed width
        self.grid_columnconfigure(1, weight=1) # Expand
        self.grid_columnconfigure(2, weight=0) # Fixed width
        
        self.grid_rowconfigure(0, weight=1)

import tkinter as tk

from View.MainApp.FileSelector import FileSelector
from View.MainApp.GraphShowcase import GraphShowcase
from View.MainApp.InfoTir import InfoTir
from View.MainApp.MenuBar import MenuBar
from View.MainApp.Feedback import Feedback

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Controller.Controller import Controller

# The view controller is the main window of the program and is in charge of the other windows
# 
class ViewController(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
    
    def set_up(self, controller:"Controller"):
        self.controller = controller
        
        # Get acces to the models
        self.data_analyser = self.controller.get_data_analyser()
        
        # Basic window creation
        self.title("FLASHy")
        self.geometry("1200x800")
        
        # Block 1: Information
        self.info_tir = InfoTir(self)
        self.info_tir.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Block 2: File Selector
        self.file_selection = FileSelector(self)
        self.file_selection.grid(row=0, column=1, sticky="nsew", padx=(0,5), pady=5)
        
        # Block 3: Graphs, Area under the curve, and Dosage
        self.graph_showcase = GraphShowcase(self)
        self.graph_showcase.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0,5), columnspan=2)
        
        # Block 4: Feedback to user
        self.feedback = Feedback(self)
        self.feedback.grid(row=2, column=0, sticky="nsew", padx=5, pady=5, columnspan=2)
        
        # Menu bar
        self.menu_bar = MenuBar(self)
        self.config(menu=self.menu_bar)
        
        self.grid_columnconfigure(0, weight=1) # Allow    horizontal mouvement
        self.grid_rowconfigure(0, weight=0)    # Restrict vertical   mouvement
        self.grid_rowconfigure(1, weight=0)    # Restrict vertical   mouvement
        self.grid_rowconfigure(2, weight=1)    # Allow    vertical   mouvement
    
    # Functions to change the paramaters of the program
    def set_rcd_len(self, value:int):
        self.controller.RECORD_LENGHT = value
    def set_pre_trigger(self, value:int):
        self.controller.PRE_TRIGGER = value
     
     
        
    # --- Useful functions for the File selector --- #   
    def send_feedback(self, text):
        return self.file_selection.insert_text_in_feedback(text)
    # ---------------------------------------------- #
    
    # --- Useful functions for the Menu Bar --- #   
    def call_file_selector(self):
        return self.file_selection.select_file()
    
    def call_open_data(self):
        print("To be implemented")
        
    def call_save_data(self):
        print("To be implemented")
        
    def call_change_rcd_len(self):
        print("To be implemented")
    
    def call_change_pre_trig(self):
        print("To be implemented")
        
    # Debug    
    def get_window_dim(self):
        print(f"Width: {self.winfo_width()}, Height: {self.winfo_height()}")
    # ----------------------------------------- #
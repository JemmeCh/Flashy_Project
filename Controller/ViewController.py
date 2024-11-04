import tkinter as tk
from tkinter import ttk

from View.FileSelector import FileSelector
from View.GraphShowcase import GraphShowcase
from View.InfoTir import InfoTir
from View.MenuBar import MenuBar
from View.Feedback import Feedback
from View.Style import FLASHyStyle

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Controller.Controller import Controller

# The view controller is the main window of the program
# 
class ViewController(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.style = FLASHyStyle(self)
    
    def set_up(self, controller:"Controller", version:str):
        self.controller = controller
        
        # Get acces to the models
        self.data_analyser = self.controller.get_data_analyser()
        
        # Basic window creation
        self.title(f"FLASHy - Version {version}")
        self.geometry("1150x925")
        
        # Block 1: Feedback to user
        self.feedback = Feedback(self)
        self.style.apply_style_tframe(self.feedback)
        self.feedback.grid(row=0, column=0, sticky="nsew", padx=5, pady=5, columnspan=2)
        
        
        
        # Block 2: Different tabs for different functionnalities
        self.tabs = ttk.Notebook(self)
        self.style.apply_style_notebook(self.tabs)
        self.tabs.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Tab 1: Informations and Bypass
        self.tab1 = ttk.Frame(self, style=self.style.tframe_style)
        self.tab1.grid(row=0, column=0, sticky="nsew")
        
        # Informations
        self.info_tir = InfoTir(self.tab1, self)
        self.style.apply_style_tframe(self.info_tir)
        self.info_tir.grid(row=0, column=0, sticky="nsew", pady=(5,0))
        
        # Bypass
        self.bypass = ttk.Frame(self.tab1, style=self.style.tframe_style)
        self.bypass.grid(row=1, column=0, sticky="nsew", pady=(5,0))
        label = ttk.Label(self.bypass, text="BYPASS!!!", style=self.style.label_style)
        label.grid(row=0, column=0)
        
        # Grid configs + adding to notebook
        self.tab1.grid_columnconfigure(0, weight=1)
        self.tab1.grid_rowconfigure(0, weight=0)
        self.tabs.add(self.tab1, text="Informations et Bypass", sticky="nsew")
        
        
        # Tab 2: CSV Reader and Analysis
        self.tab2 = ttk.Frame(self, style=self.style.tframe_style)
        self.tab2.grid(row=0, column=0, sticky="nsew")
        
        # File Selector
        self.file_selection = FileSelector(self.tab2, self)
        self.style.apply_style_tframe(self.file_selection)
        self.file_selection.grid(row=0, column=0, sticky="nsew", pady=(5,0))
        
        # Graphs, Area under the curve, and Dosage
        self.graph_showcase = GraphShowcase(self.tab2, self)
        self.style.apply_style_tframe(self.graph_showcase)
        self.graph_showcase.grid(row=1, column=0, sticky="nsew", pady=(5,0))
        
        # Grid configs + adding to notebook
        self.tab2.grid_columnconfigure(0, weight=1)
        self.tab2.grid_rowconfigure(0, weight=0)
        self.tab2.grid_rowconfigure(1, weight=0)
        self.tabs.add(self.tab2, text="Lecture CSV et Analyse", sticky="nsew")
        
             
        # Menu bar
        self.menu_bar = MenuBar(self)
        self.config(menu=self.menu_bar)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)  
    
    # Functions to change the paramaters of the program
    def set_rcd_len(self, value:int):
        self.controller.RECORD_LENGHT = value
    def set_pre_trigger(self, value:int):
        self.controller.PRE_TRIGGER = value
     
     
        
    # --- Useful functions for the File selector --- #   
    def send_feedback(self, text):
        return self.feedback.insert_text(text)
    # ---------------------------------------------- #
    
    # --- Useful functions for the Menu Bar --- #   
    def call_file_selector(self):
        return self.file_selection.select_file()
    
    def call_open_data(self):
        self.feedback.insert_text("To be implemented")
        
    def call_save_data(self):
        self.feedback.insert_text("To be implemented")
        
    def call_change_rcd_len(self):
        self.feedback.insert_text("To be implemented")
    
    def call_change_pre_trig(self):
        self.feedback.insert_text("To be implemented")
        
    # Debug    
    def get_window_dim(self):
        self.feedback.insert_text(f"Width: {self.winfo_width()}, Height: {self.winfo_height()}")
    # ----------------------------------------- #
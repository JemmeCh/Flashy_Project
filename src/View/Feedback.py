from tkinter import ttk
import tkinter as tk
from typing import TYPE_CHECKING
from datetime import datetime 

if TYPE_CHECKING:
    from src.Controller.ViewController import ViewController
    
class Feedback(ttk.Frame):
    def __init__(self, view_controller:"ViewController") -> None:
        super().__init__(view_controller, padding=(10,10), relief="raised")
        self.style = view_controller.style
        self.view_controller = view_controller
        
        self.test = ttk.Label(self, text="Feedback", style=self.style.label_style)
        self.test.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.feedback = tk.Text(self, height=3, state="disabled")
        self.feedback.grid(row=0,column=1,sticky="new",padx=5,pady=5,
                           columnspan=3)
        
        # Button to save feedback to txt
        self.save_btn = ttk.Button(self, text="Sauvegarder Feedback",
                                   command=self.save_to_txt, style=self.style.button_style)
        self.save_btn.grid(row=1, column=0, sticky="new", padx=5, pady=(0,5))
        
        # Label for project directory
        text = f"Fichier projet : {self.view_controller.controller.project_path}"
        self.project_path_label = ttk.Label(self, text=text,
                                            style=self.style.label_style)
        self.project_path_label.grid(row=1, column=1, sticky="nsew", padx=(0,5), pady=(0,5))
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
    def insert_text(self, txt:str):
        # Create time tag
        time = datetime.now()
        hour = f"{time:%H:%M:%S}"
        date = fr"{time.day}/{time.month}/{time.year}"
        time_tag = f"[ {date} | {hour} ]"
        
        message = f"{time_tag} {txt}"
        
        self.feedback.config(state="normal")
        self.feedback.insert(tk.END, "\n" + message)
        self.feedback.see(tk.END)
        self.feedback.config(state="disabled") 
        
    def save_to_txt(self):
        # Extract text from entry
        log = self.feedback.get("1.0", tk.END)
        self.view_controller.save_to_txt(log)
        
    def set_project_tag(self, path:str):
        text = f"Fichier projet : {path}"
        self.project_path_label.config(text=text)
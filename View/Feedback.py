from tkinter import ttk
import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Controller.ViewController import ViewController
    
class Feedback(ttk.Frame):
    def __init__(self, view_controller:"ViewController") -> None:
        super().__init__(view_controller, padding=(10,10), relief="raised")
        self.style = view_controller.style
        
        self.test = ttk.Label(self, text="This is a test label", style=self.style.label_style)
        self.test.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.feedback = tk.Text(self, height=3, state="disabled")
        self.feedback.grid(row=0,column=1,sticky="new",padx=5,pady=5,
                           columnspan=3)
        self.grid_columnconfigure(1, weight=1)
        
    def insert_text_in_feedback(self, txt:str):
        self.feedback.config(state="normal")
        self.feedback.insert(tk.END, txt + "\n")
        self.feedback.see(tk.END)
        self.feedback.config(state="disabled") 
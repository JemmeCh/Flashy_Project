import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import csv

class Application(tk.Tk):      
    def __init__(self) -> None:
        super().__init__()
        # Basic window creation
        self.title("FLASHy")
        self.geometry("800x600")
        
        self.info_tir = InfoTir(self)
        self.info_tir.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        self.selection = FileSelector(self)
        self.selection.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        self.grid_columnconfigure(0, weight=1) # Allow horizontal expansion
        self.grid_rowconfigure(0, weight=0) # Restrict vertical mouvement
        self.grid_rowconfigure(1, weight=0) # Restrict vertical mouvement
        


class InfoTir(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Information sur le tir", padding=(10,10), relief="raised")

        # --- Record lenght ---
        self.record_lenght = SettingEntryFrame(self, "Record Lenght", "15 000")
        self.record_lenght.grid(row=0, column=0, sticky="nswe")
        
        # --- Pre trigger ---
        self.pre_trigger = SettingEntryFrame(self, "Pre Trigger", "5 000")
        self.pre_trigger.grid(row=1, column=0, sticky="nswe")
        
        self.grid_columnconfigure(0, weight=1) # Allow column to expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        
class SettingEntryFrame(ttk.Frame):
    def __init__(self, parent, label:str, init_val:str):
        super().__init__(parent)
        
        label_width = 15 # Allign the labels
        
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


class FileSelector(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Sélection de fichier", padding=(10,10), relief="raised")
        
        self.file_name = ttk.Label(self, text="Nom du fichier:")
        self.file_name.grid(row=0,column=0,sticky="nw",padx=5,pady=5)
        
        # The user can enter a file path manually
        self.file_path = ttk.Entry(self)
        self.file_path.grid(row=0,column=1, sticky="nwe", padx=5,pady=5)
        
        self.confirm_btn = ttk.Button(self, text="Confirm path to file", 
                                      command=self.confirm_path)
        self.confirm_btn.grid(row=0,column=2, sticky="ew")
        
        self.feedback = tk.Text(self, height=1, state="disabled")
        self.feedback.grid(row=1,column=0,sticky="new",padx=5,pady=5,
                           columnspan=3)
        
        self.grid_columnconfigure(0, weight=0) # Label doesn't expand
        self.grid_columnconfigure(1, weight=1) # Entry can expand
        
        #self.grid_rowconfigure(0, weight=1)
    
    def confirm_path(self):
        self.feedback.config(state="normal")
        self.feedback.insert(tk.END, "This will be implemented later\n")
        self.feedback.config(state="disabled")
        
        
    def select_file(self) -> str:
        csv.register_dialect("CoMPASS", delimiter=';')
        
        file_path = filedialog.askopenfilename(
            title="Select the CSV file to analyse",
            filetypes=(("CSV", "*.csv"), ("All files", "*.*"))
        )
        if not file_path:
            sys.exit()
        return file_path        


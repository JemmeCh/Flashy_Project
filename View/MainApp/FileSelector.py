import csv
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Controller.ViewController import ViewController

class FileSelector(ttk.LabelFrame):
    def __init__(self, view_controller:"ViewController"):
        super().__init__(view_controller, text="Sélection de fichier", padding=(10,10), relief="raised")
        
        # Used to modify/get other parts of the program
        self.view_controller = view_controller
        
        self.file_name = ttk.Label(self, text="Nom du fichier:")
        self.file_name.grid(row=0,column=0,sticky="nw",padx=5,pady=5)
        
        # The user can enter a file path manually
        self.file_path = ttk.Entry(self)
        self.file_path.grid(row=0,column=1, sticky="nwe", padx=5,pady=5)
        
        # Confirm path inserted by user
        self.confirm_btn = ttk.Button(self, text="Confirmer", 
                                      command=self.confirm_path)
        self.confirm_btn.grid(row=0,column=2, sticky="ew")
        
        # Choose file using file explorer
        self.file_exp = ttk.Button(self, text="Ouvrir",
                                   command=self.select_file)
        self.file_exp.grid(row=0, column=3, sticky="ew")
        
        # Feedback terminal
        self.feedback = tk.Text(self, height=3, state="disabled")
        self.feedback.grid(row=1,column=0,sticky="new",padx=5,pady=5,
                           columnspan=3)
        
        # Analyse data button
        self.analyse_btn = ttk.Button(self, text="Analyser",
                                      command=self.analyse_data)
        self.analyse_btn.grid(row=1,column=3,sticky="new",pady=5)
        
        self.grid_columnconfigure(0, weight=0) # Label doesn't expand
        self.grid_columnconfigure(1, weight=1) # Entry can expand
        self.grid_columnconfigure(2, weight=0) # Confirm button doesn't expand
        self.grid_columnconfigure(3, weight=0) # Select file button doesn't expand
        self.grid_columnconfigure(3, weight=0) # Analyse button doesn't expand

        # Initialize class variables
        self.path_to_data:str = ""
    
    
    def confirm_path(self):
        self.insert_text_in_feedback("This will be implemented later")
            
    def select_file(self):
        csv.register_dialect("CoMPASS", delimiter=';')
        
        file_path = filedialog.askopenfilename(
            title="Select the CSV file to analyse",
            filetypes=(("CSV", "*.csv"), ("All files", "*.*"))
        )
        if not file_path:
            self.insert_text_in_feedback("Please select a file")
            return
        
        self.path_to_data = file_path
        
        self.insert_text_in_feedback("File selected! Checking if it's a csv...")

        if not self.check_if_csv():
            self.insert_text_in_feedback("Please select a csv file")
            return

        # Here, the file is for sure a csv file
        # Write it on the Entry
        self.file_path.delete(0,tk.END)
        self.file_path.insert(0, self.path_to_data)
        # Prompt the user that they can anaylyse the data
        self.insert_text_in_feedback(f"File {self.path_to_data} is ready to be analysed!")
        
    def check_if_csv(self) -> bool:
        return self.path_to_data.lower().endswith('.csv')
    
    def analyse_data(self):
        # Check if theres a path
        if not self.path_to_data:
            self.insert_text_in_feedback("Please select a file!")
            return
        self.insert_text_in_feedback("Reading file...")
        # Check if there's a problem when reading the CSV
        try:
            self.view_controller.data_analyser.read_file(self.path_to_data)
        except IOError as e:
            print(f"Error: {e}")
            print("The file might be in use or locked by another program.")
            return
        except StopIteration as e:
            print(f"Error: {e}")
            print("Looks like there's no header. Could be that CoMPASS is still running")
            return
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return
        self.insert_text_in_feedback("Leveling data...")
        self.view_controller.data_analyser.level_data()
        self.insert_text_in_feedback("Calculating areas under the curves...")
        self.view_controller.data_analyser.calculate_area()
        self.insert_text_in_feedback("Calculating dosage...")
        self.view_controller.data_analyser.calculate_dose()
        self.insert_text_in_feedback("Updating graphs et list...")
        self.view_controller.graph_showcase.update_pulse_graph()
        self.view_controller.graph_showcase.update_area_graph()
        self.view_controller.data_analyser.prepare_list()
        self.view_controller.graph_showcase.update_list()
        self.insert_text_in_feedback("Data analysed! Read to save analysis (to be implemented)")
        
    def insert_text_in_feedback(self, txt:str):
        self.feedback.config(state="normal")
        self.feedback.insert(tk.END, txt + "\n")
        self.feedback.see(tk.END)
        self.feedback.config(state="disabled") 
  
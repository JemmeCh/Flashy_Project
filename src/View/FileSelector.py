import csv
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.Controller.ViewController import ViewController
    from src.Model.DataAnalyser import DataAnalyser
    from src.View.GraphShowcase import GraphShowcase

class FileSelector(ttk.Frame):
    def __init__(self, parent, 
                 view_controller:"ViewController", analyser:"DataAnalyser", graph_showcase:"GraphShowcase"):
        super().__init__(parent, padding=(10,10), relief="raised")
        self.analyser = analyser
        self.graph_showcase = graph_showcase
        self.feedback = view_controller.feedback
        
        # Used to modify/get other parts of the program
        self.view_controller = view_controller
        
        self.file_name = ttk.Label(self, text="Nom du fichier:", style=self.view_controller.style.label_style)
        self.file_name.grid(row=0,column=0,sticky="nw",padx=5,pady=5)
        
        # The user can enter a file path manually
        self.file_path = ttk.Entry(self, style=self.view_controller.style.entry_style)
        self.file_path.grid(row=0,column=1, sticky="nwe", padx=5,pady=5)
        
        # Confirm path inserted by user
        # If you want, you can add it back and create its proper behavior :)
        #self.confirm_btn = ttk.Button(self, text="Confirmer", style=self.view_controller.style.button_style,
        #                              command=self.confirm_path, width=10)
        #self.confirm_btn.grid(row=0,column=2, sticky="ew", padx=(0,5),pady=5)
        
        # Choose file using file explorer
        self.file_exp = ttk.Button(self, text="Ouvrir", style=self.view_controller.style.button_style,
                                   command=self.select_file, width=10)
        self.file_exp.grid(row=0, column=3, sticky="ew", padx=(0,5),pady=5)
        
        # Analyse data button
        self.analyse_btn = ttk.Button(self, text="Analyser", style=self.view_controller.style.button_style,
                                      command=self.analyse_data_thread, width=10)
        self.analyse_btn.grid(row=0,column=4,sticky="ew",pady=5)

        self.grid_columnconfigure(0, weight=0) # Label doesn't expand
        self.grid_columnconfigure(1, weight=1) # Entry can expand
        self.grid_columnconfigure(2, weight=0) # Confirm button doesn't expand
        self.grid_columnconfigure(3, weight=0) # Select file button doesn't expand
        self.grid_columnconfigure(3, weight=0) # Analyse button doesn't expand

        # Initialize class variables
        self.path_to_data:str = ""
    
    
    def confirm_path(self):
        self.feedback.insert_text("This will be implemented later")
            
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Select the file to analyse",
            filetypes=(("CSV", "*.csv"), ("Raw", "*.dat"), ("All files", "*.*"))
        )
        if not file_path:
            self.feedback.insert_text("Please select a file")
            return
        
        self.path_to_data = file_path
        
        self.feedback.insert_text("File selected!")

        # Write it on the Entry
        self.file_path.delete(0,tk.END)
        self.file_path.insert(0, self.path_to_data)
        # Prompt the user that they can analyse the data
        self.feedback.insert_text(f"File {self.path_to_data} is ready to be analysed!")
        
    def check_if_csv(self) -> bool:
        return self.path_to_data.lower().endswith('.csv')
    
    def analyse_data_thread(self):
        """
        TODO:
        Si on utilise un Thread pour l'analyse des pulses en se moment, le programme va
        updater les graphiques et la liste en live, ce qui implique que l'utilisateur voit
        des trucs dégeulasses en live. Ça ne change rien à l'efficacité, mais le programme
        ne freeze pas. 
        
        Objectif: trouver une manière pour que les trucs dégeullases n'arrivent pas et que 
                  le programme ne freeze pas.
        
        t1 = threading.Thread(target=self.analyse_data, daemon=True)
        t1.start()
        """
        self.analyse_data()
    
    def analyse_data(self):
        # Check if theres a path
        if not self.path_to_data:
            self.feedback.insert_text("Please select a file!")
            return
        self.feedback.insert_text("Reading file...")
        # Check if there's a problem when reading the file
        try:
            result = self.analyser.read_file(self.path_to_data)
            if not result:
                return
        except IOError as e:
            self.feedback.insert_text(f"Error: {e}")
            self.feedback.insert_text("The file might be in use or locked by another program.")
            return
        except StopIteration as e:
            self.feedback.insert_text(f"Error: {e}")
            self.feedback.insert_text("Looks like there's no header. Could be that CoMPASS is still running")
            return
        except Exception as e:
            self.feedback.insert_text(f"An unexpected error occurred: {e}")
            raise e
            return
        
        self.feedback.insert_text("Leveling data...")
        self.analyser.level_data()
        self.feedback.insert_text("Calculating areas under the curves...")
        self.analyser.calculate_area()
        self.feedback.insert_text("Calculating dosage...")
        self.analyser.calculate_dose()
        self.feedback.insert_text("Updating graphs et list...")
        self.graph_showcase.update_pulse_graph()
        self.graph_showcase.update_area_graph()
        self.analyser.prepare_list()
        self.graph_showcase.update_list()
        self.feedback.insert_text("Data analysed!")
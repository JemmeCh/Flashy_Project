import sys
import csv

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from typing import Literal

# For graphs, I'm using matplotlib
import matplotlib
from matplotlib import pyplot as plt

from DataAnalyser import DataAnalyser 
matplotlib.use('TkAgg')
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.backend_bases import key_press_handler

import numpy as np

class Application(tk.Tk):      
    def __init__(self) -> None:
        super().__init__()
        # Setting the DataAnalyser
        self.dataAnalyser = DataAnalyser(self)
        
        # Parameters of the recording
        self.RECORD_LENGHT:int = 0
        #self.SAMPLE_SIZE:int = 0
        self.PRE_TRIGGER:int = 0
        
        # Basic window creation
        self.title("FLASHy")
        self.geometry("1200x800")
        
        # Block 1: Information
        self.info_tir = InfoTir(self)
        self.info_tir.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Block 2: File Selector
        self.selection = FileSelector(self)
        self.selection.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Block 3: Graphs, Area under the curve, and Dosage
        self.graph_view = GraphShowcase(self)
        self.graph_view.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        
        # Block 4: Saving analysed data
        
        # Menu bar
        self.menu_bar = MenuBar(self)
        self.config(menu=self.menu_bar)
        
        self.grid_columnconfigure(0, weight=1) # Allow    horizontal mouvement
        self.grid_rowconfigure(0, weight=0)    # Restrict vertical   mouvement
        self.grid_rowconfigure(1, weight=0)    # Restrict vertical   mouvement
        self.grid_rowconfigure(2, weight=1)    # Allow    vertical   mouvement
        
    # --- Useful functions for the File selector --- #   
    def send_feedback(self, text):
        return self.selection.insert_text_in_feedback(text)
    # ---------------------------------------------- #  
    
    # --- Useful functions for changing/getting experiment parameters --- #
    def get_rcd_len(self) -> int:
        return self.RECORD_LENGHT
    def set_rcd_len(self, x: int) -> None:
        self.RECORD_LENGHT = x
    def get_pre_trigger(self) -> int:
        return self.PRE_TRIGGER
    def set_pre_trigger(self, x:int) -> None:
        self.PRE_TRIGGER
    # ------------------------------------------------------------------- #   
    
    # --- Useful functions for the Menu Bar --- #   
    def call_file_selector(self):
        return self.selection.select_file()
    
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
    
    # --- Useful functions for the Graph section --- #
    
    # ---------------------------------------------- #
        


class InfoTir(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Information sur le tir", padding=(10,10), relief="raised")

        # --- Record lenght ---
        self.record_lenght = SettingEntryFrame(self, "Record Lenght", "15 000")
        self.record_lenght.grid(row=0, column=0, sticky="nswe")
        parent.set_rcd_len(15000)
        
        # --- Pre trigger ---
        self.pre_trigger = SettingEntryFrame(self, "Pre Trigger", "5 000")
        self.pre_trigger.grid(row=1, column=0, sticky="nswe")
        parent.set_pre_trigger(5000)
        
        self.grid_columnconfigure(0, weight=1) # Allow column to expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
# Used for creating a parameter
# TODO: Make it so you can change those values       
class SettingEntryFrame(ttk.Frame):
    def __init__(self, parent, label:str, init_val:str):
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


class FileSelector(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Sélection de fichier", padding=(10,10), relief="raised")
        
        # Used to modify/get other parts of the program
        self.app = parent
        
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
        #TODO: Check if theres a path

        self.insert_text_in_feedback("Reading file...")
        self.app.dataAnalyser.read_file(self.path_to_data)
        self.insert_text_in_feedback("Leveling data...")
        self.app.dataAnalyser.level_data()
        self.insert_text_in_feedback("Calculation areas under the curves...")
        self.app.dataAnalyser.calculate_area()
        self.insert_text_in_feedback("Updating graphs et list...")
        self.app.graph_view.update_pulse_graph()
        self.app.graph_view.update_area_graph()
        self.app.graph_view.update_list()
        self.insert_text_in_feedback("Data analysed! Read to save analysis (to be implemented)")
        
    def insert_text_in_feedback(self, txt:str):
        self.feedback.config(state="normal")
        self.feedback.insert(tk.END, txt + "\n")
        self.feedback.see(tk.END)
        self.feedback.config(state="disabled") 
    
  
  
class MenuBar(tk.Menu):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Analyse menu
        analyse_menu = tk.Menu(self, tearoff=0)
        analyse_menu.add_command(label="Nouvelle Analyse", 
                              command=lambda: parent.call_file_selector())
        analyse_menu.add_command(label="Ouvrir Analyse",
                              command=lambda: parent.call_open_data())
        analyse_menu.add_command(label="Sauvegarder Analyse",
                                 command=lambda: parent.call_save_data())
        self.add_cascade(label="Analyse", menu=analyse_menu)
        
        # Settings menu
        setting_menu = tk.Menu(self, tearoff=0)
        setting_menu.add_command(label="Changer Record Lenght",
                              command=lambda: parent.call_change_rcd_len())
        setting_menu.add_command(label="Changer Pre Trigger",
                              command=lambda: parent.call_change_pre_trig())
        self.add_cascade(label="Préférence", menu=setting_menu)
        
        # Debug program
        debug_menu = tk.Menu(self, tearoff=0)
        debug_menu.add_command(label="Get window dimentions",
                               command=lambda: parent.get_window_dim())
        self.add_cascade(label="Debug", menu=debug_menu)
        
        # Close program
        self.add_command(label="Fermer", command=lambda: self.exit(parent))
        
        
    def exit(self, parent) -> None:
        # Do a pop-up confirmation
        check = CustomDialog(parent, "Quitter le programme?", "Oui", "Non")
        if check.result:
            parent.quit()


# Used for confirming quitting the program via the Menu bar
class CustomDialog(tk.Toplevel):
    def __init__(self, parent, message:str, yes_text:str, no_text:str):
        super().__init__(parent)
        self.geometry("+100000+100000")
        self.result = None
        self.title("Confirmer fermeture") 
        
        # Create the label for the message
        label = tk.Label(self, text=message)
        label.pack(pady=10)

        # Create Yes button
        yes_button = ttk.Button(self, text=yes_text, command=self.on_yes)
        yes_button.pack(side="left", padx=20, pady=20)

        # Create No button
        no_button = ttk.Button(self, text=no_text, command=self.on_no)
        no_button.pack(side="right", padx=20, pady=20)
        
        # Centered on the parent's window
        self.center_window(parent)
        
        # Wait for the window to close
        self.transient(parent)
        self.grab_set()
        self.wait_window(self)
        
    def center_window(self, parent) -> None:
        self.update_idletasks()  # Ensure window is updated to get the correct size
        popup_width = self.winfo_reqwidth()
        popup_height = self.winfo_reqheight()

        # Get the parent window's position and size
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()

        # Calculate position for the popup to be centered
        center_x = parent_x + (parent_width // 2) - (popup_width // 2)
        center_y = parent_y + (parent_height // 2) - (popup_height // 2)

        # Set the position of the popup window
        self.geometry(f"+{center_x}+{center_y}")

    def on_yes(self) -> None:
        self.result = True
        self.destroy()  # Close the dialog

    def on_no(self) -> None:
        self.result = False
        self.destroy()  # Close the dialog
   
     
class GraphShowcase(ttk.Labelframe):
    def __init__(self, parent) -> None:
        super().__init__(parent, text="Résultat de l'analyse", padding=(10,10), relief="raised")
        
        # Used to modify/get other parts of the program
        self.app = parent
        #TODO: 
        # - link it to the data
        
        # Pulses' forms graph
        self.pulse_graph = PulseGraph(self, "Temps (microseconde)", "Voltage (V)", 
                                          False)
        self.pulse_graph.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        if hasattr(self.pulse_graph, 'toolbar'):
            self.pulse_graph.toolbar.grid(row=1, column=0, sticky="ew")
        
        # Area per pulse graph
        self.area_graph = AreaGraph(self, "Temps (microseconde)", "Voltage (V)", 
                                          False)
        self.area_graph.canvas.get_tk_widget().grid(row=2, column=0, sticky="nsew")
        if hasattr(self.area_graph, 'toolbar'):
            self.area_graph.toolbar.grid(row=3, column=0, sticky="ew", pady=20)
        
        # List of results spanning both rows
        self.list = ListOfResults(self)
        self.list.grid(row=0,column=1, rowspan=4, sticky="nsew")
        
        # Configure row/column weight for grid responsiveness
        self.grid_rowconfigure(0, weight=1)  # First graph row
        self.grid_rowconfigure(2, weight=1)  # Second graph row
        self.grid_columnconfigure(0, weight=1)  # Left column (both graphs)
        self.grid_columnconfigure(1, weight=1)  # Right column (spanning list)
        
    def update_pulse_graph(self):
        self.pulse_graph.update_graph()
    def update_area_graph(self):
        self.area_graph.update_graph()
    def update_list(self): 
        self.list.update_list()
        
    def fetch_pulse_info(self):
        return self.app.dataAnalyser.get_pulse_info()
    def fetch_t_axis(self):
        return self.app.dataAnalyser.get_t_axis()
    def fetch_area_under_curve(self):
        return self.app.dataAnalyser.get_area_under_curve()
    def fetch_nbr_of_pulse(self):
        return self.app.dataAnalyser.get_nbr_of_pulse()
        
        
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
        
               
class Graph:
    def __init__(self, parent, x_label:str, y_label:str, 
                 toolbar:bool) -> None:
        self.create_plot_canvas(parent,x_label,y_label)
        
        self.showcase = parent
        self.x_label = x_label
        self.y_label = y_label
        self.toolbar_bool = toolbar
        
        #self.canvas.draw()
        # Plot holder
        self.x = np.arange(25)
        self.y = np.arange(25)
        self.line, = self.ax.plot(self.x, self.y)
        #self.ax.plot(self.x, self.y)
        
        # Tool bar
        if toolbar:
            self.toolbar = NavigationToolbar2Tk(self.canvas, parent, pack_toolbar=False)
            self.toolbar.update()
            self.toolbar.grid(row=1, column=0, sticky="n")
        
        # Some test
        #self.canvas.mpl_connect("key_press_event", self.on_key_press)
        self.canvas.mpl_connect("key_press_event", key_press_handler) # type: ignore
    
    def create_plot_canvas(self, parent, x_label:str, y_label:str,):
        # Create a new figure and axis
        self.fig = Figure(figsize=(6,5))
        self.ax = self.fig.add_subplot()
        self.ax.set_xlabel(x_label)
        self.ax.set_ylabel(y_label)
        self.fig.tight_layout()
        self.ax.set_autoscale_on(True)
        self.ax.set_adjustable('datalim')
        self.ax.autoscale(True, 'both')
        
        # Creating canvas where plot is drawn
        if hasattr(self, 'canvas'):  # If canvas already exists, destroy it
            self.canvas.get_tk_widget().destroy()

        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        

    # The other Graph classes must change this
    def update_graph(self):
        pass  
    
    def on_key_press(self, event):
        print(f"you pressed {event.key}")
        
class PulseGraph(Graph):
    def __init__(self, parent, x_label:str, y_label:str, 
                 toolbar:bool):
        super().__init__(parent, x_label, y_label, toolbar)
        
        self.x = self.showcase.fetch_t_axis()
        self.y = self.showcase.fetch_pulse_info()
        
    def update_graph(self):
        # Clear the old canvas
        self.create_plot_canvas(self.showcase,self.x_label,self.y_label)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        
        # Get the new values of x and y
        self.x = self.showcase.fetch_t_axis()
        self.y = self.showcase.fetch_pulse_info()
        self.x = np.array(self.x)
        self.y = np.array(self.y)

        # Update plot
        self.ax.clear()
        for pulse in self.y:
            self.ax.plot(self.x, pulse)

        self.ax.autoscale_view()
        
        self.canvas.draw()
              
class AreaGraph(Graph):
    def __init__(self, parent, x_label:str, y_label:str, 
                 toolbar:bool):
        super().__init__(parent, x_label, y_label, toolbar)
        self.showcase = parent
        self.x = self.showcase.fetch_nbr_of_pulse()
        self.y = self.showcase.fetch_area_under_curve()
        
    def update_graph(self):
        # Clear the old canvas
        self.create_plot_canvas(self.showcase,self.x_label,self.y_label)
        self.canvas.get_tk_widget().grid(row=2, column=0, sticky="nsew")

        
        # Get the new values of x and y
        self.x = self.showcase.fetch_nbr_of_pulse()
        self.y = self.showcase.fetch_area_under_curve()
        self.x = np.arange(self.x)
        self.y = np.array(self.y)
        
        # Update plot
        self.ax.clear()
        self.ax.plot(self.x, self.y,'ro',linestyle='dashed',markersize=10)

        self.ax.autoscale_view()
        
        self.canvas.draw()
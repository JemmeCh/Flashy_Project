import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING

from uri_template import expand

if TYPE_CHECKING:
    from Controller.ViewController import ViewController

class InfoTir(ttk.Frame):
    def __init__(self, parent, view_controller:"ViewController"):
        super().__init__(parent, padding=(10,10), relief="raised")
        style = view_controller.style
        self.view_controller = view_controller
        # Style used
        self.label_style = style.label_style
        self.button_style = style.button_style
        self.entry_style = style.entry_style
        self.tframe_style = style.tframe_style
        self.apply_style_notebook = style.apply_style_notebook
        
        self.tabs = ttk.Notebook(self)
        self.apply_style_notebook(self.tabs)
        self.tabs.grid(row=0, column=0, sticky="nesw")
        
        # Heading and editable_columns across all trees
        self.heading_CoMPASS = ("Paramètres", "Board", "Channel 0", "Channel 1")
        self.editable_columns_CoMPASS = [1,2] # Board and Channel 0
        self.heading_FLASHy = ("Paramètres", "Choix")
        self.editable_columns_FLASHy = [1] # Only "Choix"
        
        # Tab 1: Input
        self.input_frame = ttk.Frame(self, style=self.tframe_style)
        self.input_frame.grid(row=0, column=0, sticky="nsew")
        self.input_tree = ParameterTreeview(self.input_frame, columns=self.heading_CoMPASS,
                                            show="headings", editable_columns=self.editable_columns_CoMPASS)
        self.input_tree.grid(row=0, column=0, sticky="nsew")
        self.tabs.add(self.input_frame, text="Input", sticky="nsew")
        
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_rowconfigure(0, weight=1)
        
        # Tab 2: Analyse
        self.analyse_frame = ttk.Frame(self, style=self.tframe_style)
        self.analyse_frame.grid(row=0, column=0, sticky="nsew")
        self.analyse_tree = ParameterTreeview(self.analyse_frame, columns=self.heading_FLASHy,
                                            show="headings", editable_columns=self.editable_columns_FLASHy)
        self.analyse_tree.grid(row=0, column=0, sticky="nsew")
        self.tabs.add(self.analyse_frame, text="Analyse", sticky="nsew")
        
        self.analyse_frame.grid_columnconfigure(0, weight=1)
        self.analyse_frame.grid_rowconfigure(0, weight=1)     
           
        # Configure all columns of trees
        for col in self.heading_CoMPASS:
            # Input
            self.input_tree.heading(col, text=col)
            self.input_tree.column(col, anchor="center", stretch=True)
        for col in self.heading_FLASHy:
            # Analyse
            self.analyse_tree.heading(col, text=col)
            self.analyse_tree.column(col, anchor="center", stretch=True)
        
        # Make input parameters
        input_parameters = [
            ("Record Lenght (ns)", "15000", "", ""),
            ("Pre-trigger (ns)", "5000", "5000", ""),
            ("Polarity", "Positive", "Positive", ""),
            ("DC Offset (%)", "5.000", "5.000", ""),
            ("Coarse gain", "3x", "3x", ""),
        ]
        for row in input_parameters:
            self.input_tree.insert("", "end", values=row)
            
        # Make analyse parameters
        analyse_parameters = [
            ("Méthode du calcul d'aire", "trap"),
            ("Méthode de mise à niveau", "dynamic-median"),
            ("Graphique 1", "Pulse"),
            ("Graphique 2", "Aire"),
            ("Facteur de conversion: [V*s] --> [C]", "1 / 33.33"),
            ("Facteur de conversion: Aires --> Doses", "2")
        ]
        for row in analyse_parameters:
            self.analyse_tree.insert("", "end", values=row)
            
        # Grid configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
class ParameterTreeview(ttk.Treeview):
    def __init__(self, parent, editable_columns=None, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Store editable columns
        self.editable_columns = editable_columns
        # Track the currently edited cell
        self.editing = None 
        
        # Add editing behavior
        self.bind("<Double-1>", self.start_edit)

    def start_edit(self, event):
        region = self.identify("region", event.x, event.y)
        if region != "cell":
            return
        
        row_id = self.identify_row(event.y)
        col_id = self.identify_column(event.x)
        col_index = int(col_id.replace("#", "")) - 1  # Convert column ID to 0-based index

        # Skip non-editable columns
        if self.editable_columns is not None \
            and col_index not in self.editable_columns:
            return
        
        # Set up for Entry widget
        self.editing = (row_id, col_id)
        current_value = self.item(row_id, "values")[col_index]
        x, y, width, height = self.bbox(row_id, col_id)

        # Create an Entry widget for editing
        self.entry = tk.Entry(self, width=width) # type: ignore
        self.entry.place(x=x, y=y, width=width, height=height)
        self.entry.insert(0, current_value)
        self.entry.focus()
        
        # To stop editing Entry
        self.bind_widget(self.entry, self.finish_edit_entry)

    def finish_edit_entry(self, event):
        if not self.editing:
            return
        
        row_id, col_id = self.editing
        col_index = int(col_id.replace("#", "")) - 1
        new_value = self.entry.get()
        values = list(self.item(row_id, "values"))
        values[col_index] = new_value
        self.item(row_id, values=values)

        # Cleanup
        self.entry.destroy()
        self.editing = None

    def bind_widget(self, widget, function):
        widget.bind("<Return>", function)
        widget.bind("<FocusOut>", function)
        widget.bind("<Escape>", function)

    def set_editable_columns(self, editable_columns):
        self.editable_columns = editable_columns



if __name__ == "__main__":
    root = tk.Tk()
    root.title("Editable Treeview Example")
    root.geometry("500x400")
    
    columns = ("Parameter", "Value1", "Value2", "Value3")
    tree = ParameterTreeview(root, columns=columns, 
                             show="headings", 
                             editable_columns=[1, 2])
    
    # Configure columns
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")
    tree.pack(fill="both", expand=True)
    
    # Populate with data
    data = [
        ("Parameter A", "123", "456", "789"),
        ("Parameter B", "234", "567", "890"),
        ("Parameter C", "345", "678", "901"),
    ]
    for row in data:
        tree.insert("", "end", values=row)
    
    root.mainloop()

    
    
    
    
    
"""     def __init__(self, parent, view_controller:"ViewController"):
        super().__init__(parent, padding=(10,10), relief="raised")
        # Acces to view_controller stuff
        self.style = view_controller.style
        
        # --- Record lenght ---
        self.record_lenght = SettingEntryFrame(self, "Record Lenght", '15000')
        self.record_lenght.grid(row=0, column=0, sticky="nswe")
        view_controller.set_rcd_len('15000')
        
        # --- Pre trigger ---
        self.pre_trigger = SettingEntryFrame(self, "Pre Trigger", "5000")
        self.pre_trigger.grid(row=1, column=0, sticky="nswe")
        view_controller.set_pre_trigger('5000')
        
        self.grid_columnconfigure(0, weight=1) # Allow column to expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

# Used for creating a parameter
# TODO: Make it so you can change those values       
class SettingEntryFrame(ttk.Frame):
    def __init__(self, parent:InfoTir, label:str, init_val:str):
        super().__init__(parent, style=parent.style.tframe_style)
        
        label_width = 15 # Align the labels
        
        self.label_recLen = ttk.Label(self, text=label, width=label_width, style=parent.style.label_style)
        self.label_recLen.grid(row=0, column=0, sticky="w",padx=5, pady=5)
        
        self.record_lenght = ttk.Entry(self, style=parent.style.entry_style)
        self.record_lenght.insert(0, init_val)
        self.record_lenght.config(state="readonly") 
        self.record_lenght.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        self.unit_recLen = ttk.Label(self, text="ns", style=parent.style.label_style)
        self.unit_recLen.grid(row=0, column=2, sticky="w",padx=5, pady=5)

        self.grid_columnconfigure(0, weight=0) # Fixed width
        self.grid_columnconfigure(1, weight=1) # Expand
        self.grid_columnconfigure(2, weight=0) # Fixed width
        
        self.grid_rowconfigure(0, weight=1)
 """
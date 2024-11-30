import tkinter as tk
from tkinter import ttk
import numpy as np
from typing import TYPE_CHECKING

if __name__ == "__main__":
    from Style import FLASHyStyle
else:
    from View.Style import FLASHyStyle

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
        self.input_tree = ParameterTreeview(self.input_frame, self.view_controller,
                                            columns=self.heading_CoMPASS, selectmode='none',
                                            show="headings", editable_columns=self.editable_columns_CoMPASS)
        self.input_tree.grid(row=0, column=0, sticky="nsew")
        self.tabs.add(self.input_frame, text="Input", sticky="nsew")
        
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_rowconfigure(0, weight=1)
        
        # Tab 2: Analyse
        self.analyse_frame = ttk.Frame(self, style=self.tframe_style)
        self.analyse_frame.grid(row=0, column=0, sticky="nsew")
        self.analyse_tree = ParameterTreeview(self.analyse_frame, self.view_controller,
                                              columns=self.heading_FLASHy,selectmode='none',
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
        self.input_tree.set_matrix_map(
            [
                ["Title", "Entry", "Entry", "Entry"],
                ["Title", "Entry", "Entry", "Entry"],
                ["Title", ("Positive", "Negative(?)"), ("Positive", "Negative(?)"), ("Positive", "Negative(?)")],
                ["Title", "Entry", "Entry", "Entry"],
                ["Title", ("Please leave it at 3x", "1x", "3x", "5x", "10x"), ("Please leave it at 3x", "1x", "3x", "5x", "10x"), ("Please leave it at 3x", "1x", "3x", "5x", "10x")],
            ]
        )
        
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
        self.analyse_tree.set_matrix_map(
            [
                ["Title", ("naif", "trap")],
                ["Title", ("median", "dynamic-mean", "dynamic-median")],
                ["Title", ("Please dont change me", "Pulse", "Aire")],
                ["Title", ("Please dont change me", "Pulse", "Aire")],
                ["Title", "Entry"],
                ["Title", "Entry"]
            ]
        )
        
        # Grid configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
class ParameterTreeview(ttk.Treeview):
    def __init__(self, parent, view_controller:"ViewController"=None, editable_columns=None, **kwargs): # type: ignore
        super().__init__(parent, **kwargs)
        self.view_controller = view_controller
        if self.view_controller:
            self.feedback = view_controller.send_feedback
            self.controller = view_controller.controller
            self.style = view_controller.style
        else:
            self.style = FLASHyStyle(parent)
        self.editing_widget = None
        
        # Right-click menu definition
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Utiliser Board (CH0 et CH1)", command=lambda: self.set_parameter('Board'))
        self.menu.add_command(label="Utiliser CH0 seulement", command=lambda: self.set_parameter('CH0'))
        self.menu.add_command(label="Utiliser CH1 seulement", command=lambda: self.set_parameter('CH1'))
        self.menu.add_command(label="Utiliser valeur par défaut", command=lambda: self.set_parameter('default'))
        
        # Store editable columns
        self.editable_columns = editable_columns
        # Track the currently edited cell
        self.editing = None 
        # Track the right click target
        self.right_click_target = None
        
        # Add editing behavior
        self.bind("<Double-1>", self.start_edit)
        self.bind("<Button-3>", self.show_context_menu)
        
        # Set up tags
        self.tag_configure('Board', background=self.style.WHITE)
        self.tag_configure('CH0', background=self.style.LIGHT_GRAY)
        self.tag_configure('CH1', background=self.style.GRAY)
        self.tag_configure('default', background=self.style.BLACK)
        
    """Functions for editing a parameter"""
    def start_edit(self, event):
        region = self.identify("region", event.x, event.y)
        if region != "cell":
            return
        
        row_id = self.identify_row(event.y)
        col_id = self.identify_column(event.x)
        row_index = int(row_id.replace("I", "")) - 1  # Convert row    ID to 0-based index
        col_index = int(col_id.replace("#", "")) - 1  # Convert column ID to 0-based index

        # Skip non-editable columns
        if self.editable_columns is not None \
            and col_index not in self.editable_columns:
            return
        
        if self._has_default_tag(row_id):
            if self.view_controller:
                self.feedback("This parameter is deactivated")
            else:
                print("This parameter is deactivated")
            return
        
        self.editing = (row_id, col_id)
        current_value = self.item(row_id, "values")[col_index]
        x, y, width, height = self.bbox(row_id, col_id)
        
        # Set up which widget to use
        choice = self.matrix_map[row_index][col_index]
        if choice == "Title":
            print("...what have you done for this to happen")
        elif choice == "Entry":
            self.editing_widget = self.create_entry_widget(current_value, x, y, width, height)
            self.bind_entry_events()
        else:
            self.editing_widget = self.create_combobox_widget(choice, current_value, x, y, width, height)
            self.bind_combobox_events()

    def create_entry_widget(self, current_value, x, y, width, height):
        entry = tk.Entry(self, width=width)  # type: ignore
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, current_value)
        entry.focus()
        return entry

    def bind_entry_events(self):
        self.editing_widget.bind("<Return>", self.finish_edit_entry) # type: ignore
        self.editing_widget.bind("<FocusOut>", self.cancel_edit) # type: ignore
        self.editing_widget.bind("<Escape>", self.cancel_edit) # type: ignore

    def create_combobox_widget(self, options, current_value, x, y, width, height):
        combobox = ttk.Combobox(self, width=width, values=options)  # type: ignore
        combobox.place(x=x, y=y, width=width, height=height)
        combobox.set(current_value)
        combobox.focus()
        return combobox

    def bind_combobox_events(self):
        self.editing_widget.bind("<<ComboboxSelected>>", self.finish_edit_combobox) # type: ignore
        self.editing_widget.bind("<Return>", self.finish_edit_combobox) # type: ignore
        self.editing_widget.bind("<FocusOut>", self.delayed_finish_combobox) # type: ignore
        self.editing_widget.bind("<Escape>", self.cancel_edit) # type: ignore
             
    def finish_edit_combobox(self, event):
        if not self.editing:
            return
        
        row_id, col_id = self.editing
        self.col_index = int(col_id.replace("#", "")) - 1
        self.row_index = int(row_id.replace("I", "")) - 1
        
        new_value = self.editing_widget.get() # type: ignore
        
        # Check if the value is in the choices
        if new_value not in self.matrix_map[self.row_index][self.col_index]:
            print("new values not in choices, try again")
            return
        
        values = list(self.item(row_id, "values"))
        self.old_value = values[self.col_index]
        values[self.col_index] = new_value
        self.item(row_id, values=values)

        # Cleanup
        self.cleanup()
    
    def delayed_finish_combobox(self, event):
        try:
            if self.focus_get() != self.editing_widget:
                self.after(100, self.finish_edit_combobox(event)) # type: ignore
        except KeyError: # Supress the annoying error 
            pass
            
    def finish_edit_entry(self, event):
        if not self.editing:
            return
        
        row_id, col_id = self.editing
        self.col_index = int(col_id.replace("#", "")) - 1
        self.row_index = int(row_id.replace("I", "")) - 1
        new_value = self.editing_widget.get() # type: ignore
        values = list(self.item(row_id, "values"))
        self.old_value = values[self.col_index]
        values[self.col_index] = new_value
        self.item(row_id, values=values)

        # Cleanup
        self.cleanup()
        
    def cancel_edit(self, event):
        if self.editing_widget:
            self.old_value = self.editing_widget.get()
        self.cleanup()
        
    def cleanup(self):
        if self.editing_widget:
            new_value = self.editing_widget.get()
            self.editing_widget.destroy()
            self.editing_widget = None
            
            # Send new value to controller
            row_id, col_id = self.editing # type:ignore
            self.col_index = int(col_id.replace("#", "")) - 1
            parameter_modified = list(self.item(row_id, "values"))[0]
            if self.view_controller:
                # Check if the parameter can be modified
                if self.controller.map_parameters.__contains__(parameter_modified):
                    self.controller.map_parameters[parameter_modified] = new_value
                    self.feedback(f"Parameter '{parameter_modified}' set to {new_value}")
                else:
                    self.feedback(f"'{parameter_modified}' has no equivalent in the Controller class. You need to map it in the source code (and make it change the program's behavior accordingly)")
                    values = list(self.item(row_id, "values"))
                    values[self.col_index] = self.old_value
                    self.item(row_id, values=values)
        # Reset for further uses
        self.old_value = ""
        self.editing = None
    
    """Functions for the context menu"""
    def show_context_menu(self, event):
        row_id = self.identify_row(event.y)
        col_id = self.identify_column(event.x)
        col_index = int(col_id.replace("#", "")) - 1
        row_index = int(row_id.replace("I", "")) - 1

        title = self.matrix_map[row_index][col_index]

        # Check if the user right clicked the parameter column
        if title == "Title":
            self.right_click_target = (row_id, col_id)
            self.menu.post(event.x_root, event.y_root)
            
    def set_parameter(self, selection):
        if self.right_click_target:
            row_id, _ = self.right_click_target
            row_index = int(row_id.replace("I", "")) - 1
            
            # Change color of the background according to the selection
            # ['default': black, 'Board': white, 'CH0': light_gray, 'CH1': gray]
            if selection == 'Board':
                self.item(self.right_click_target[0], tags='Board')
                self.row_tags[row_index] = 'Board' 
            elif selection == 'CH0':
                self.item(self.right_click_target[0], tags='CH0')
                self.row_tags[row_index] = 'CH0'
            elif selection == 'CH1':
                self.item(self.right_click_target[0], tags='CH1')
                self.row_tags[row_index] = 'CH1'
            else: # 'default'
                self.item(self.right_click_target[0], tags='default')
                self.row_tags[row_index] = 'default'
            self.right_click_target = None
    
    def _has_default_tag(self, row_id:str) -> bool:
        """
        True --> has the tag 'default' or no tag \n
        False --> doesn't have the 'default' tag """
        try:
            tag = self.item(row_id, option='tags')[0]
            return True if tag == 'default' else False
        except IndexError:
            print("This item has no tags")
            return True
                    
    def set_matrix_map(self, matrix_map):
        self.nbr_rows = len(self.get_children())  # Count of rows (exclude header)
        self.nbr_columns = len(self["columns"])  # Count of columns
        
        self.matrix_map = matrix_map
        
        # Set the tags
        self.row_tags:list[str] = []
        for row in self.get_children():
            self.item(row, tags='Board')
            self.row_tags.append('Board')
    
    def set_editable_columns(self, editable_columns):
        self.editable_columns = editable_columns

    def get_row_tags(self) -> list[str]:
        return self.row_tags

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Editable Treeview Example")
    root.geometry("500x400")
    
    columns = ("Parameter", "Value1", "Value2", "Value3")
    tree = ParameterTreeview(root, columns=columns, 
                             show="headings", 
                             editable_columns=[1, 2],
                              selectmode='none')
    
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
    matrix_map =[
        ["Title", "Entry", "Entry", "Entry"],
        ["Title", "Entry", "Entry", "Entry"],
        ["Title", ("1", "2"), ("3", "4"), ("5", "6")]
    ]
    
    # Create matrix map of entrys or option menu
    tree.set_matrix_map(matrix_map)
    
    root.mainloop()
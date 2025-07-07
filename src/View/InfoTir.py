import tkinter as tk
from tkinter import ttk, messagebox
from typing import TYPE_CHECKING, Literal, Tuple

if __name__ == "__main__":
    from Style import FLASHyStyle
else:
    from src.View.Style import FLASHyStyle

if TYPE_CHECKING:
    from src.Controller.Controller import Controller
    from src.Controller.ViewController import ViewController

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
        self.editable_columns_CoMPASS = [1,2,3] # Board, Channel 0, Channel 1
        self.heading_FLASHy = ("Paramètres", "Choix")
        self.editable_columns_FLASHy = [1] # Only "Choix"
        
        # Tab 1: Input
        self.input_frame = ttk.Frame(self, style=self.tframe_style)
        self.input_frame.grid(row=0, column=0, sticky="nsew")
        self.input_tree = ParameterTreeview(self.input_frame, self.view_controller.get_input_parameters(),
                                            self.view_controller,
                                            columns=self.heading_CoMPASS, selectmode='none',
                                            show="headings", editable_columns=self.editable_columns_CoMPASS)
        self.input_tree.grid(row=0, column=0, sticky="nsew")
        self.tabs.add(self.input_frame, text="Input", sticky="nsew")
        
        self.input_frame.grid_columnconfigure(0, weight=1)
        self.input_frame.grid_rowconfigure(0, weight=1)
        
        # Tab 2: Discriminator
        self.discriminator_frame = ttk.Frame(self, style=self.tframe_style)
        self.discriminator_frame.grid(row=0, column=0, sticky="nsew")
        self.discriminator_tree = ParameterTreeview(self.discriminator_frame, self.view_controller.get_discr_parameters(),
                                                    self.view_controller,
                                            columns=self.heading_CoMPASS, selectmode='none',
                                            show="headings", editable_columns=self.editable_columns_CoMPASS)
        self.discriminator_tree.grid(row=0, column=0, sticky="nsew")
        self.tabs.add(self.discriminator_frame, text="Discriminator", sticky="nsew")
        
        self.discriminator_frame.grid_columnconfigure(0, weight=1)
        self.discriminator_frame.grid_rowconfigure(0, weight=1)
         
        # Tab 3: Trapezoid
        self.trapezoid_frame = ttk.Frame(self, style=self.tframe_style)
        self.trapezoid_frame.grid(row=0, column=0, sticky="nsew")
        self.trapezoid_tree = ParameterTreeview(self.trapezoid_frame, self.view_controller.get_trapezoid_parameters(),
                                                self.view_controller,
                                            columns=self.heading_CoMPASS, selectmode='none',
                                            show="headings", editable_columns=self.editable_columns_CoMPASS)
        self.trapezoid_tree.grid(row=0, column=0, sticky="nsew")
        self.tabs.add(self.trapezoid_frame, text="Trapezoid", sticky="nsew")
        
        self.trapezoid_frame.grid_columnconfigure(0, weight=1)
        self.trapezoid_frame.grid_rowconfigure(0, weight=1)
        """ Most of these settings are used in CoMPASS only as internal settings.
        The only useful tab could be the tabs 7 and 8. I didn't set them up since I ran out of time.
        If you understand how the preview tabs are made, then you can easily implement them.
        # Tab 4: Spectra
        self.spectra_frame = ttk.Frame(self, style=self.tframe_style)
        self.spectra_frame.grid(row=0, column=0, sticky="nsew")
        self.spectra_tree = ParameterTreeview(self.spectra_frame, self.view_controller,
                                            columns=self.heading_CoMPASS, selectmode='none',
                                            show="headings", editable_columns=self.editable_columns_CoMPASS)
        self.spectra_tree.grid(row=0, column=0, sticky="nsew")
        self.tabs.add(self.spectra_frame, text="Spectra", sticky="nsew")
        
        self.spectra_frame.grid_columnconfigure(0, weight=1)
        self.spectra_frame.grid_rowconfigure(0, weight=1)
        
        # Tab 5: Rejection
        self.rejection_frame = ttk.Frame(self, style=self.tframe_style)
        self.rejection_frame.grid(row=0, column=0, sticky="nsew")
        self.rejection_tree = ParameterTreeview(self.rejection_frame, self.view_controller,
                                            columns=self.heading_CoMPASS, selectmode='none',
                                            show="headings", editable_columns=self.editable_columns_CoMPASS)
        self.rejection_tree.grid(row=0, column=0, sticky="nsew")
        self.tabs.add(self.rejection_frame, text="Rejection", sticky="nsew")
        
        self.rejection_frame.grid_columnconfigure(0, weight=1)
        self.rejection_frame.grid_rowconfigure(0, weight=1)
        
        # Tab 6: Energy calibration
        self.energy_calibration_frame = ttk.Frame(self, style=self.tframe_style)
        self.energy_calibration_frame.grid(row=0, column=0, sticky="nsew")
        self.energy_calibration_tree = ParameterTreeview(self.energy_calibration_frame, self.view_controller,
                                            columns=self.heading_CoMPASS, selectmode='none',
                                            show="headings", editable_columns=self.editable_columns_CoMPASS)
        self.energy_calibration_tree.grid(row=0, column=0, sticky="nsew")
        self.tabs.add(self.energy_calibration_frame, text="Energy calibration", sticky="nsew")
        
        self.energy_calibration_frame.grid_columnconfigure(0, weight=1)
        self.energy_calibration_frame.grid_rowconfigure(0, weight=1)
        
        # Tab 7: Synchronization
        self.synchronization_frame = ttk.Frame(self, style=self.tframe_style)
        self.synchronization_frame.grid(row=0, column=0, sticky="nsew")
        self.synchronization_tree = ParameterTreeview(self.synchronization_frame, self.view_controller,
                                            columns=self.heading_CoMPASS, selectmode='none',
                                            show="headings", editable_columns=self.editable_columns_CoMPASS)
        self.synchronization_tree.grid(row=0, column=0, sticky="nsew")
        self.tabs.add(self.synchronization_frame, text="Synchronization", sticky="nsew")
        
        self.synchronization_frame.grid_columnconfigure(0, weight=1)
        self.synchronization_frame.grid_rowconfigure(0, weight=1)
        
        # Tab 8: Trigger/Veto/Coincidences
        self.tvc_frame = ttk.Frame(self, style=self.tframe_style)
        self.tvc_frame.grid(row=0, column=0, sticky="nsew")
        self.tvc_tree = ParameterTreeview(self.tvc_frame, self.view_controller,
                                            columns=self.heading_CoMPASS, selectmode='none',
                                            show="headings", editable_columns=self.editable_columns_CoMPASS)
        self.tvc_tree.grid(row=0, column=0, sticky="nsew")
        self.tabs.add(self.tvc_frame, text=r"Trigger/Veto/Coincidences", sticky="nsew")
        
        self.tvc_frame.grid_columnconfigure(0, weight=1)
        self.tvc_frame.grid_rowconfigure(0, weight=1)
         """
        # Tab -1: Analyse
        self.analyse_frame = ttk.Frame(self, style=self.tframe_style)
        self.analyse_frame.grid(row=0, column=0, sticky="nsew")
        self.analyse_tree = ParameterTreeview(self.analyse_frame, self.view_controller.get_analyse_parameters(),
                                              self.view_controller,
                                              columns=self.heading_FLASHy,selectmode='none',
                                              show="headings", editable_columns=self.editable_columns_FLASHy,
                                              analyse=True)
        self.analyse_tree.grid(row=0, column=0, sticky="nsew")
        self.tabs.add(self.analyse_frame, text="Analyse", sticky="nsew")
        
        self.analyse_frame.grid_columnconfigure(0, weight=1)
        self.analyse_frame.grid_rowconfigure(0, weight=1)     
           
        # Configure all columns of trees
        for col in self.heading_CoMPASS:
            # Input
            self.input_tree.heading(col, text=col)
            self.input_tree.column(col, anchor="center", stretch=True)
            # Discriminator
            self.discriminator_tree.heading(col, text=col)
            self.discriminator_tree.column(col, anchor="center", stretch=True)
            # Trapezoid
            self.trapezoid_tree.heading(col, text=col)
            self.trapezoid_tree.column(col, anchor="center", stretch=True)
            """# Spectra
            self.spectra_tree.heading(col, text=col)
            self.spectra_tree.column(col, anchor="center", stretch=True)
            # Rejection
            self.rejection_tree.heading(col, text=col)
            self.rejection_tree.column(col, anchor="center", stretch=True)
            # Energy calibration
            self.energy_calibration_tree.heading(col, text=col)
            self.energy_calibration_tree.column(col, anchor="center", stretch=True)
            # Syncronization
            self.synchronization_tree.heading(col, text=col)
            self.synchronization_tree.column(col, anchor="center", stretch=True)
            # Trigger/Veto/Coincidences
            self.tvc_tree.heading(col, text=col)
            self.tvc_tree.column(col, anchor="center", stretch=True) """
        for col in self.heading_FLASHy:
            # Analyse
            self.analyse_tree.heading(col, text=col)
            self.analyse_tree.column(col, anchor="center", stretch=True)
        
        # Make input parameters
        for row in self.view_controller.get_input_parameters().values():
            self.input_tree.insert("", "end", values=row.get_row())
        self.input_tree.set_tags()
        
        # Make discriminator parameters
        for row in self.view_controller.get_discr_parameters().values():
            self.discriminator_tree.insert("","end", values=row.get_row())
        self.discriminator_tree.set_tags()
        
        # Make trapezoid parameters
        for row in self.view_controller.get_trapezoid_parameters().values():
            self.trapezoid_tree.insert("","end", values=row.get_row())
        self.trapezoid_tree.set_tags()
        
        """ # Make spectra parameters
        for row in self.view_controller.get_spectra_parameters().values():
            self.spectra_tree.insert("","end", values=row.get_row())
        self.spectra_tree.set_tags() """
        
        # Make analyse parameters
        for row in self.view_controller.get_analyse_parameters().values():
            self.analyse_tree.insert("", "end", values=row.get_row())
        self.analyse_tree.set_tags()
        # As you can see, anaylyse_tree doesnt have a validation_ranges since I didnt have the time to make one specific to it.
        # I'd recommend using the analyse boolean to your advantage :)
        
        # Grid configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
class ParameterTreeview(ttk.Treeview):
    def __init__(self, parent, parameters:dict[str, "Parameter"], view_controller:"ViewController"=None, analyse:bool=False, editable_columns=None, **kwargs): # type: ignore
        super().__init__(parent, **kwargs)
        self.view_controller = view_controller
        self.feedback = view_controller.send_feedback
        self.controller = view_controller.controller
        self.style = view_controller.style
        
        # Dictionnary of parameters associated with this tree
        self.parameters = parameters
        # If the tab is the analyse tab
        self.analyse = analyse
        
        # Right-click menu definition
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Utiliser Board (CH0 et CH1)", command=lambda: self.set_parameter('board'))
        self.menu.add_command(label="Utiliser CH0 seulement", command=lambda: self.set_parameter('CH0'))
        self.menu.add_command(label="Utiliser CH1 seulement", command=lambda: self.set_parameter('CH1'))
        self.menu.add_command(label="Utiliser valeur par défaut", command=lambda: self.set_parameter('default'))
        
        # Store editable columns
        self.editable_columns = editable_columns
        # Track the currently edited cell and widget
        self.editing = None 
        self.editing_widget = None
        # Track the right click target
        self.right_click_target = None
        # Track the tooltip widget + delayed job
        self.hover_label = None
        self.is_hovering = None
        #self.hover_job = None 
        
        # Add editing behavior
        self.bind("<Double-1>", self.start_edit)
        self.bind("<Button-3>", self.show_context_menu)
        self.bind("<Motion>", self.on_hover)
        self.bind("<Leave>", self.hide_description)
        
        # Set up tags
        self.set_tags()
        if not self.analyse:
            self.tag_configure('board', background=self.style.WHITE)
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
            self.feedback("This parameter is deactivated")
            return
        
        self.editing = (row_id, col_id)
        current_value = self.item(row_id, "values")[col_index]
        parameter = self.item(row_id, 'values')[0]
        x, y, width, height = self.bbox(row_id, col_id)
        
        # Set up which widget to use
        widget_type = self.parameters[parameter].get_widget_type()
        if widget_type == "entry":
            self.editing_widget = self.create_entry_widget(current_value, x, y, width, height)
            self.bind_entry_events()
        elif widget_type == "combobox":
            self.editing_widget = self.create_combobox_widget(self.parameters[parameter], current_value, x, y, width, height)
            self.bind_combobox_events()
        else:
            self.feedback("...what have you done for this to happen")

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

    def create_combobox_widget(self, parameter, current_value, x, y, width, height):
        combobox = ttk.Combobox(self, width=width, values=parameter.get_choices())
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
        parameter = self.item(row_id, 'values')[0]
        
        # Check if the value is in the choices
        if new_value not in self.parameters[parameter].get_choices(): # type: ignore
            self.feedback("New value not in the choices, try again")
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
        new_value = self.editing_widget.get().strip() # type: ignore
        parameter = self.item(row_id, 'values')[0]
        
        if self.validate_input(self.parameters[parameter], new_value):
            values = list(self.item(row_id, "values"))
            self.old_value = values[self.col_index]
            values[self.col_index] = new_value
            self.item(row_id, values=values)
        else:
            try:
                self.feedback(f"Value for '{parameter}' must be a number between {self.parameters[parameter].get_valide_range()[0]} and {self.parameters[parameter].get_valide_range()[1]}.")
                self.invalid_entry_imput()
            except TypeError:
                self.feedback(f"Value for '{parameter}' doesn't have a range to be checked. The shown value is hard-coded")
                
                return

        # Cleanup
        self.cleanup()
        
    def validate_input(self, parameter, value):
        try:
            value = float(value)
            min_val, max_val = parameter.get_valide_range() # type: ignore
            return min_val <= value <= max_val
        except ValueError:
            return False # Not a number
        except TypeError:
            return True # parameter.get_valide_range() gives None
        
    def cancel_edit(self, event):
        if self.editing_widget:
            self.old_value = self.editing_widget.get().strip()
        self.cleanup()
        
    def cleanup(self):
        if self.editing_widget:
            new_value = self.editing_widget.get().strip()
            self.editing_widget.destroy()
            self.editing_widget = None
            
            # Send new value to controller
            row_id, col_id = self.editing # type:ignore
            self.col_index = int(col_id.replace("#", "")) - 1
            if self.col_index == 1 and not self.analyse:
                col = 'board'
            elif self.col_index == 2:
                col = 'CH0'
            elif self.col_index == 3:
                col = 'CH1'
            else:
                col = 'choice'
            parameter_modified = list(self.item(row_id, "values"))[0]
            if self.validate_input(self.parameters[parameter_modified], new_value) \
                or self.parameters[parameter_modified].get_choices().__contains__(new_value):
                self.controller.set_parameter_value(parameter_modified, new_value, self.col_index)
                self.feedback(f"Parameter '{parameter_modified}' set to {new_value} (for '{col}')")
            else:
                self.feedback(f"'{parameter_modified}' is invalid.")
                values = list(self.item(row_id, "values"))
                values[self.col_index] = self.old_value
                self.item(row_id, values=values)
        # Reset for further uses
        self.old_value = ""
        self.editing = None
        
    def invalid_entry_imput(self):
        if self.editing_widget:
            self.editing_widget.destroy()
            self.editing_widget = None
        self.old_value = ""
        self.editing = None
    
    """Functions for the context menu"""
    def show_context_menu(self, event):
        row_id = self.identify_row(event.y)
        col_id = self.identify_column(event.x)
        col_index = int(col_id.replace("#", "")) - 1
        row_index = int(row_id.replace("I", "")) - 1

        # Check if the user right clicked the parameter column
        if col_index == 0 and not self.analyse:
            self.right_click_target = (row_id, col_id)
            self.menu.post(event.x_root, event.y_root)
            
    def set_parameter(self, selection):
        if self.right_click_target:
            row_id, _ = self.right_click_target
            row_index = int(row_id.replace("I", "")) - 1
            parameter = list(self.item(row_id, "values"))[0]
            
            # Change color of the background according to the selection
            # ['default': black, 'board': white, 'CH0': light_gray, 'CH1': gray]
            if selection == 'board':
                self.item(self.right_click_target[0], tags='board')
                self.row_tags[row_index] = 'board' 
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
            self.feedback(f"'{parameter}' set to '{self.row_tags[row_index]}' use")
            self.controller.set_parameter_state(parameter, self.row_tags[row_index]) # type:ignore
    
    def _has_default_tag(self, row_id:str) -> bool:
        """
        True --> has the tag 'default' or no tag \n
        False --> doesn't have the 'default' tag """
        try:
            tag = self.item(row_id, option='tags')
            return True if tag[0] == 'default' else False
        except IndexError:
            self.feedback("This item has no tags")
            return True
    
    """Functions for the parameter's description"""
    def on_hover(self, event):
        row_id = self.identify_row(event.y)
        col_id = self.identify_column(event.x)
        
        if col_id == '#1' and row_id:
            if self.is_hovering != row_id:
                self.is_hovering = row_id
                parameter = self.item(row_id, "values")[0]
                description = self.parameters[parameter].get_description()
                self.show_description(event.x_root, event.y_root, description)
            else:
                parameter = self.item(row_id, "values")[0]
                description = self.parameters[parameter].get_description()
                self.show_description(event.x_root, event.y_root, description)
        else:
            self.hide_description(event)
    
    """ Couldn't make this work...
     def schedule_description(self, event, col_id, description):
        if self.hover_job:
            self.after_cancel(self.hover_job)
        self.hover_job = self.after(300, lambda: self.show_description(event.x_root, event.y_root, description))
        if self.identify_column(event.x) != col_id:
            self.after_cancel(self.hover_job) """
    
    def show_description(self, x, y, description):
        if not self.hover_label:
            self.hover_label = tk.Toplevel(self)
            self.hover_label.wm_overrideredirect(True)
            self.hover_label.attributes("-topmost", True)
            self.label = tk.Label(self.hover_label, text=description, justify='left', background="#e8faff", relief='solid', borderwidth=1)
            self.label.pack()
        else:
            self.label.config(text=description)
        self.hover_label.geometry(f'+{x+10}+{y+10}')
    
    def hide_description(self, event=None):
        if self.hover_label:
            self.hover_label.destroy()
            self.hover_label = None
        self.is_hovering = None
        #self.hover_job = None
    
    """Miscellaneous"""                
    def set_tags(self):
        self.row_tags:list[str] = []
        for row in self.get_children():
            self.item(row, tags='board')
            self.row_tags.append('board')
         
    def set_editable_columns(self, editable_columns):
        self.editable_columns = editable_columns

    def get_row_tags(self) -> list[str]:
        return self.row_tags

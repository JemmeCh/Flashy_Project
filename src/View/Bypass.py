import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING, Any, Dict

import threading

# To install the module: pip install caen-felib
from caen_felib import lib, device, error

if TYPE_CHECKING:
    from src.Controller.ViewController import ViewController
    from src.View.Style import FLASHyStyle
    
class Bypass(ttk.Frame):
    def __init__(self, parent, view_controller:"ViewController"):
        super().__init__(parent, padding=(10,10), relief="raised")
        
        # Access to view_controller stuff
        self.style = view_controller.style
        self.config(style=self.style.tframe_style)
        self.view_controller = view_controller
        self.send_feedback = view_controller.send_feedback
        
        # Get digitizer functions
        self.get_basic_dig_info = view_controller.digitizer.get_basic_dig_info
        self.arm_digitizer = view_controller.digitizer.arm_digitizer
        
        # --- Section 1: Info on digitizer ---
        self.dig_info_panel = DigitizerInfoPanel(self, self.style)
        self.dig_info_panel.grid(row=0, column=0, sticky='new')
        
        self.seperator = ttk.Separator(self, orient='vertical')
        self.seperator.grid(row=0,column=1, rowspan=5, padx=(10,10), pady=2, sticky="nsew")
        
        # --- Section 2: Status and data acquisition ---
        self.data_aqc_panel = DataAQCPanel(self, self.style)
        self.data_aqc_panel.grid(row=0, column=2, sticky='new')
        
        # Configuration of the whole panel
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)        
    
"""SECTION 1: INFO ON DIGITIZER"""
class DigitizerInfoPanel(ttk.Frame):
    """ttk.Frame containing all the information about the digitizer. 
    All fields are not modifiable by the user (READ_ONLY paramaters)

    Args:
        ttk (Bypass(ttk.Frame)): Frame that contains all the Bypass related stuff
        ttk (FLASHyStyle(ttk.Style)): Style of the program
    """
    def __init__(self, bypass_frame:"Bypass", style:"FLASHyStyle"):
        super().__init__(bypass_frame, style=style.tframe_style)
        # Style used
        self.label_style = style.label_style
        self.button_style = style.button_style
        self.entry_style = style.entry_style
        
        self.bypass_frame = bypass_frame
        
        # Frame label
        self.frame_label = ttk.Label(self, text="Information sur le Digitizer", justify='center',
                                     style=self.label_style)
        self.frame_label.grid(row=0, column=0, sticky='nsew')
        self.grid_rowconfigure(0, weight=1)
        
        # Model name
        self.model_name = BoardInfoContainer(self, "Model name", style=self.entry_style)
        self.model_name.grid(row=1, column=0, sticky='new')
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Family code
        self.family_code = BoardInfoContainer(self, "Family code", style=self.entry_style)
        self.family_code.grid(row=1, column=1, sticky='new')
        self.grid_columnconfigure(1, weight=1)
        
        # Serial Number
        self.serial_num = BoardInfoContainer(self, "Serial Number", style=self.entry_style)
        self.serial_num.grid(row=1, column=2, sticky='new')
        self.grid_columnconfigure(2, weight=1)
        
        # ADC n bits
        self.adc_n_bits = BoardInfoContainer(self, "ADC n bits", style=self.entry_style)
        self.adc_n_bits.grid(row=2, column=0, sticky='new')
        self.grid_rowconfigure(2, weight=1)
        
        # ADC sample rate (in Msps)
        self.adc_samplrate_msps = BoardInfoContainer(self, "Sample rate (in Msps)", style=self.entry_style)
        self.adc_samplrate_msps.grid(row=2, column=1, sticky='new')
        
        # Sampling period (in ns)
        self.sampling_period_ns = BoardInfoContainer(self, "Sampling (in ns)", style=self.entry_style)
        self.sampling_period_ns.grid(row=2, column=2, sticky='new')
        
        # Firware type
        self.fw_type = BoardInfoContainer(self, "Firmware type", style=self.entry_style)
        self.fw_type.grid(row=3, column=0, sticky='new')
        self.grid_rowconfigure(3, weight=1)
        
        # Max raw data size
        self.max_rawdata_size = BoardInfoContainer(self, "Max raw data size", style=self.entry_style)
        self.max_rawdata_size.grid(row=3, column=1, sticky='new',
                                     columnspan=2)
        
        # ID
        
        # Link
        
        # ROC firmware
        
        # AMC firmware
        
        # License
        
        
        # Connect Button
        self.connect_btn = ttk.Button(self, style=self.button_style, width=10,
                                      command=self.get_basic_dig_info, 
                                      text="Connecter au Digitizer")
        self.connect_btn.grid(row=5, column=0, columnspan=5, sticky="nsew", pady=(5,0))
        
        # Configuration of the whole panel
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        
    
    def dispatch_data(self, data: Dict[str, Any]):
        def update_entry(entry_widget, value):
            entry_widget.config(state="normal")
            entry_widget.delete(0, 'end')
            entry_widget.insert(tk.END, str(value))
            entry_widget.config(state="readonly")
        
        # Define the functions for each element
        def change_model_name(value: str):
            update_entry(self.model_name.entry, value)
        def change_family_code(value: str):
            update_entry(self.family_code.entry, value)
        def change_fw_type(value: str):
            update_entry(self.fw_type.entry, value)
        def change_serial_num(value: int):
            update_entry(self.serial_num.entry, value)
        def change_adc_n_bits(value: int):
            update_entry(self.adc_n_bits.entry, value)
        def change_adc_samplrate_msps(value: float):
            update_entry(self.adc_samplrate_msps.entry, value)
        def change_sampling_period_ns(value: int):
            update_entry(self.sampling_period_ns.entry, value)
        def change_max_rawdata_size(value: float):
            update_entry(self.max_rawdata_size.entry, value)

        # Map element names to functions
        function_map = {
            'model_name': change_model_name,
            'family_code': change_family_code,
            'fw_type': change_fw_type,
            'serial_num': change_serial_num,
            'adc_n_bits': change_adc_n_bits,
            'adc_samplrate_msps': change_adc_samplrate_msps,
            'sampling_period_ns': change_sampling_period_ns,
            'max_rawdata_size': change_max_rawdata_size
        }

        # Dispatch data to the appropriate functions
        for element, value in data.items():
            method = function_map.get(element)
            if method:
                method(value)
            else:
                self.bypass_frame.send_feedback(f"Method '{element}' doesn't exist. Value is {value}")

    def get_basic_dig_info(self):
        t1 = threading.Thread(target=self.bypass_frame.get_basic_dig_info, daemon=True)
        t1.start()
               
class BoardInfoContainer(ttk.Frame):
    def __init__(self, frame:DigitizerInfoPanel, label:str, *args, **kwargs):
        """Creates a board information container of format
            Label: Entry
        """
        super().__init__(frame, *args, **kwargs)
        self.frame = frame
        
        # Label
        self.label = ttk.Label(self, style=self.frame.label_style, text=label, width=20)
        self.label.grid(row=0,column=0,sticky="nsew")
        
        # Entry
        self.entry = ttk.Entry(self, style=self.frame.entry_style, state='readonly')
        self.entry.grid(row=0,column=1,sticky="nsew")
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

"""SECTION 2: STATUS AND DATA ACQUISITION"""
class DataAQCPanel(ttk.Frame):
    def __init__(self, bypass_frame:"Bypass", style:"FLASHyStyle"):
        super().__init__(bypass_frame, style=style.tframe_style)
        self.bypass_frame = bypass_frame
        
        # Style used
        self.tframe_style = style.tframe_style
        self.label_style = style.label_style
        self.entry_style = style.entry_style
        #self.checkbox_style = style.checkbox_style
        self.button_style = style.button_style
        
        # Frame label
        self.frame_label = ttk.Label(self, text="Prise de mesure", justify='center',
                                     style=self.label_style)
        self.frame_label.grid(row=0, column=0, sticky='new')
        self.grid_rowconfigure(0, weight=1)
        
        # Status
        # Format is [Status: (text in entry)]
        self.status_frame = ttk.Frame(self, style=self.tframe_style)
        
        self.status_label = ttk.Label(self.status_frame, style=self.label_style,
                                      text="Status:")
        self.status_label.grid(row=0, column=0,sticky="w",padx=(0,5))
        self.status_text = ttk.Entry(self.status_frame, style=self.entry_style)
        self.status_text.insert(0, "Déconnecté")
        self.status_text.config(state="readonly") 
        self.status_text.grid(row=0, column=1, sticky="ew")
        
        self.status_frame.grid(row=1, column=0,sticky="new")
        self.status_frame.rowconfigure(0, weight=1)       
        self.status_frame.grid_columnconfigure(0, weight=0)
        self.status_frame.grid_columnconfigure(1, weight=1)
        
        # Arm digitizer
        # Format is [Armer Digitizer: (checkbox)]
        self.arm_dig_frame = ttk.Frame(self, style=self.tframe_style)
        
        self.arm_dig_label = ttk.Label(self.arm_dig_frame, style=self.label_style,
                                       text="Armer Digitizer:")
        self.arm_dig_label.grid(row=0, column=0,sticky="w",padx=(0,5))
        self.arm_dig_check = Checkbox(self.arm_dig_frame, # TODO: style
                                             command=self.arm_digitizer,
                                             state="disabled")
        self.arm_dig_check.grid(row=0, column=1,sticky='ew')
        
        self.arm_dig_frame.grid(row=2, column=0, sticky='new')
        self.arm_dig_frame.grid_rowconfigure(0, weight=1)
        self.arm_dig_frame.grid_columnconfigure(0, weight=0)
        self.arm_dig_frame.grid_columnconfigure(1, weight=1)
        
        # Run ID + increment
        self.name_frame = ttk.Frame(self, style=self.tframe_style)
        
        self.name_label = ttk.Label(self.name_frame, style=self.label_style,
                                    text='Nom:')
        self.name_label.grid(row=0, column=0, sticky='w', padx=(0,5))
        self.name_entry = ttk.Entry(self.name_frame, style=self.entry_style)
        self.name_entry.insert(0, self.bypass_frame.view_controller.get_name_of_shoot())
        self.name_entry.grid(row=0, column=1, sticky='ew', padx=(0,5))
        self.name_btn = ttk.Button(self.name_frame, style=self.button_style,
                                   text='Confirmer', command=self.confirm_name)
        self.name_btn.grid(row=0, column=2, sticky='ew')
        
        self.name_frame.grid(row=4, column=0, sticky='nwe', pady=(0,5))
        self.name_frame.grid_rowconfigure(0, weight=1)
        self.name_frame.grid_columnconfigure(0, weight=1)
        self.name_frame.grid_columnconfigure(1, weight=1)
        self.name_frame.grid_columnconfigure(2, weight=1)
        
        # Record button
        self.record_frame = ttk.Frame(self, style=self.tframe_style)
        
        self.record_button = Recordbutton(self.record_frame, self.bypass_frame,
                                        style=self.button_style,
                                        text="Commencer mesure")
        self.record_button.grid(row=0, column=0,sticky='nsew')
        
        self.record_frame.grid(row=5, column=0, sticky='nsew', pady=(0,5))
        self.record_frame.grid_rowconfigure(0, weight=1)
        self.record_frame.grid_columnconfigure(0, weight=1)
        
        # Configuration of the whole panel
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        
    def change_aqc_panel_status(self, message:str):
        self.status_text.config(state='normal')
        self.status_text.delete(0, 'end')
        self.status_text.insert(tk.END, message)
        self.status_text.config(state='readonly')
        
    def arm_digitizer(self):
        t1 = threading.Thread(target=self.bypass_frame.arm_digitizer, daemon=True)
        t1.start() 
        
    def confirm_name(self):
        new_name = self.name_entry.get().strip()
        if new_name != '':
            if not self.bypass_frame.view_controller.controller.isRECORDING:
                self.bypass_frame.view_controller.set_name_of_shoot(new_name)
                self.bypass_frame.send_feedback(f"Name of shoot set to '{new_name}'")
                return
            else: # Data is being recorded
                self.bypass_frame.view_controller.send_feedback(f'Data is being recorded!')
                self.name_entry.insert(0, self.bypass_frame.view_controller.get_name_of_shoot())
                return
        else:
            self.bypass_frame.send_feedback("Please put a name!")
            self.name_entry.insert(0, self.bypass_frame.view_controller.get_name_of_shoot())
            return

class Checkbox(ttk.Checkbutton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.variable = tk.BooleanVar(self)
        self.config(variable=self.variable)

    def checked(self):
        return self.variable.get()

    def check(self):
        self.variable.set(True)

    def uncheck(self):
        self.variable.set(False)

class Recordbutton(ttk.Button):
    def __init__(self, record_frame, bypass_frame, **args):
        super().__init__(record_frame, **args)
        self.send_feedback = bypass_frame.send_feedback
        self.record_data = bypass_frame.view_controller.digitizer.record_data
        self.isRECORDING = False
        self.configure(command=self.toggle_recording, width=30)
        
        self.controller = bypass_frame.view_controller.controller
                
    def toggle_recording(self):
        if self.isRECORDING: self.stop_recording()
        else: self.start_recording()
        
    def start_recording(self):
        self.isRECORDING = True
        self.config(text='Arrêter mesure')
        self.send_feedback("Début de l'enregistrement...")
        self.t1 = threading.Thread(target=self.record_data, daemon=True)
        self.t1.start()
        
    def stop_recording(self):
        self.isRECORDING = False
        self.controller.isRECORDING = False
        self.config(text='Commencer mesure')
        self.send_feedback("Enregistrement terminé!")
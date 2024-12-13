from typing import Any, Dict, List, Literal, Tuple

import os
from datetime import datetime
import pickle
import numpy as np
import csv

import re
from collections import defaultdict
from ast import literal_eval
from tkinter import filedialog

from src.Controller.ModelController import ModelController
from src.Controller.ViewController import ViewController
from src.Model.DataAnalyser import DataAnalyser
from src.Model.Digitizer import Digitizer
from src.Model.Error import Error

# This class contains all the different settings of the program and
# is used as a link between the models and the views
class Controller():
    def __init__(self, view_controller:ViewController, model_controller:ModelController) -> None:
        self.view_controller = view_controller
        self.model_controller = model_controller
        self.error_handling = Error(self)

        # Get/Generate parameters
        self.load_parameters_on_open()
        self.load_internal_parameters_on_open()

        # Bool that determines the state of the program
        self.isCONNECTING_TO_DIG:bool = False
        self.isTAKING_DATA:bool = False
        self.isCHANGING_SETTINGS:bool = False
        self.isGETTING_BASIC_INFO: bool = False
        self.isRECORDING:bool = False
        
        self.hasDIGITIZERCONNECTED: bool = False
        
        # Which channel are we using? 
        self.channel_use = 'CH0' # ['CH0', 'CH1', 'both']
        
        # Set basic parameters
        self.ADC_NBIT:int = 14 # For DT5781
        
    
    # Getting information from the models
    def get_data_analyser(self) -> DataAnalyser:
        return self.model_controller.get_data_analyser()
    def get_ch0_analyser(self) -> DataAnalyser:
        return self.model_controller.get_ch0_analyser()
    def get_ch1_analyser(self) -> DataAnalyser:
        return self.model_controller.get_ch1_analyser()
    def get_raw_analyser(self) -> DataAnalyser:
        return self.model_controller.get_raw_analyser()
    def get_digitizer(self) -> Digitizer:
        return self.model_controller.get_digitizer()
    
    def set_ADC_NBIT(self, val:int):
        self.ADC_NBIT = val
        
    # Determines if the digitizer can be used
    def can_use_dig(self):
        if self.isCONNECTING_TO_DIG or self.isCHANGING_SETTINGS \
        or self.isTAKING_DATA or self.isGETTING_BASIC_INFO \
        or self.isRECORDING:
            return False
        return True
    
    # Used by exception handeling
    def change_states(self):
        self.isCONNECTING_TO_DIG:bool = False
        self.isTAKING_DATA:bool = False
        self.isCHANGING_SETTINGS:bool = False
        self.isGETTING_BASIC_INFO: bool = False
        if self.isRECORDING:
            self.view_controller.bypass.data_aqc_panel.record_button.stop_recording()    
        self.isRECORDING = False
    
    # From models to views
    def send_feedback(self, message:str):
        self.view_controller.send_feedback(message)
    def dispatch_data(self, data:Dict[str, Any]):
        self.view_controller.bypass.dig_info_panel.dispatch_data(data)
    def change_aqc_panel_status(self, message:str):
        self.view_controller.bypass.data_aqc_panel.change_aqc_panel_status(message)
    
    def get_RECORD_LENGHT(self) -> str:
        return self.input_parameters["Record Lenght (ns)"].get_row()[1]
    def get_AREA_CALCULATION_METHOD(self) -> str:
        return self.analyse_parameters["Méthode du calcul d'aire"].get_row()[1]
    def get_LEVELING_METHOD(self) -> str:
        return self.analyse_parameters["Méthode de mise à niveau"].get_row()[1]
    def get_DOSE_FACTOR(self) -> float:
        return float(self.analyse_parameters["Facteur de conversion: [nC] --> [cGy]"].get_row()[1])
    def get_COARSEGAIN(self) -> float:
        # Maps the according option to its value
        # 10Vpp‐3Vpp‐1Vpp‐0.3Vpp
        coarse_map:dict[str,float] = {
            "COARSE_GAIN_X1"  : 10,   # 10  Vpp
            "COARSE_GAIN_X3"  : 3,    # 3   Vpp
            "COARSE_GAIN_X10" : 1,    # 1   Vpp
            "COARSE_GAIN_X33" : 0.3,  # 0.3 Vpp
        }
        # Get board setting NOTE: Change this logic if you want to use CH1
        choice = self.input_parameters["Coarse gain"].get_row()[1]
        
        return coarse_map[choice]
    def get_ADC_NBIT(self) -> int:
        return self.ADC_NBIT
    
    """ Functions for changing parameters """
    def _set_parameter(self, name:str, action:str, *args):
        for param_dict in self.parameters_tuple:
            if name in param_dict:
                if hasattr(param_dict[name], action):
                    getattr(param_dict[name], action)(*args)
                else:
                    self.send_feedback(f"{name} doesn't support the action '{action}'")
                return
        self.send_feedback(f"Couldn't find {name} in the list of parameters")
    
    def set_parameter_value(self, name:str, value:str, index:int):
        self._set_parameter(name, 'set_row', value, index)
    def set_parameter_state(self, name:str, state:Literal['board', 'CH0', 'CH1', 'default']):
        self._set_parameter(name, 'change_state', state)
    
    def get_dig_parameters(self) -> Dict[str, "Parameter"]:
        return self.input_parameters | self.discr_parameters | self.trapezoid_parameters
    
    """Functions for saving files"""
    def create_instance_directory(self):
        try:
            os.mkdir(self.path_to_instance)
        except FileExistsError:
            pass # The program was closed and reopen. We want to use the same directory
        except PermissionError:
            print(f"Permission denied: Unable to create '{self.path_to_instance}'.")
    def create_shoot_directory(self):
        try:
            os.mkdir(self.path_of_shoot)
        except FileExistsError:
            pass # The program was closed and reopen. We want to use the same directory
        except PermissionError:
            print(f"Permission denied: Unable to create '{self.path_of_shoot}'.")
    def set_name_of_shoot(self, name:str):
        # Tries to create directory
        potential_name = f'{name}_{str(1)}'
        try:
            path_of_shoot = os.path.join(self.path_to_instance, potential_name)
            os.mkdir(path_of_shoot) # Check if we can create a directory with the name
            self.path_of_shoot = path_of_shoot
            self.increment = 1
            self.name_of_shoot = f'{name}'.replace(' ', '')
            self.incremented_name = f"{name.replace(' ', '')}_{self.increment}"
        except FileExistsError:
            # Failed to create it
            self.send_feedback(f'The directory {name} already exists')
            return
    def increment_name_of_shoot(self):
        self.increment += 1
        self.incremented_name = f'{self.name_of_shoot}_{str(self.increment)}'
        self.path_of_shoot = os.path.join(self.path_to_instance, self.incremented_name)
        try:
            os.mkdir(self.path_of_shoot)
        except FileExistsError:
            self.send_feedback(f"'{self.path_of_shoot}' already exists! You should change the name of the shoot to not override old data")
    def get_increment(self):
        return self.increment
    def get_name_of_shoot(self):
        return self.name_of_shoot
    
    def save_to_txt(self, txt:str):
        time = datetime.now()
        hour = f"{time:%H-%M-%S}"
        date = fr"{time.day}-{time.month}-{time.year}"
        file_name = f'log_{date}_{hour}.txt'
        path = os.path.join(self.path_to_feedback, file_name)
        try:
            with open(path, 'w') as file:
                file.write(txt)
            self.send_feedback(f"Log saved at/as '{path}' successfully!")
        except IOError as e:
            self.send_feedback(e.__str__())
            self.send_feedback("Creating 'Feedback' directory")
            os.mkdir(self.path_to_feedback)
            self.save_to_txt(txt)
        except Exception as e:
            self.send_feedback("failed saving feedback")
            self.send_feedback(e.__str__())
    def save_raw_data(self, all_detect, channel:str):
        file_name = f"{self.incremented_name}_{channel}.dat"
        path = os.path.join(self.path_of_shoot, file_name)
        try:
            with open(path, 'wb') as file:
                for element in all_detect:
                    pickle.dump(element, file)
        except Exception as e:
            self.send_feedback('failed saving raw data')
            self.send_feedback(e.__str__())
    def save_to_csv(self, pulses, channel):
        file_name = f"{self.incremented_name}_{channel}-DETECTED.csv"
        path = os.path.join(self.path_of_shoot, file_name)
        try:
            writter = csv.writer(open(path, 'w', newline=''))
            writter.writerow(pulses[0])
            for pulse in pulses[1:]:
                #print(pulse)
                channel = pulse[0]
                flag = pulse[1]
                waveform = pulse[2]
                samples = pulse[3].tolist()
                list = [channel, flag, waveform, samples]
                
                writter.writerow(list)
        except Exception as e:
            self.send_feedback('failed csv save')
            self.send_feedback(e.__str__())
    def triage_data(self, channel_pulses, channel):
        pulses = []
        pulses.append(['Channel', 'Flag', 'Waveform_size', 'Samples'])
        
        # Extract samples only
        for new_pulse in channel_pulses:
            # Clean data
            form = np.reshape(new_pulse[3], (1, int(new_pulse[-2])))
            clean = self.get_data_analyser().clean_data(form)
            if not len(clean) == 0: # Select only pulses
                reconstruct = [new_pulse[0], new_pulse[1], new_pulse[2], clean]
                pulses.append(reconstruct)
        self.save_to_csv(pulses, channel)
        return pulses
    
    """Function for when data has been collected"""
    def post_acquisition(self, all_detect):
        """
        all_detect: contient toute les pulses pris par le digitizer
        [[
            channel.copy(), flags.copy(), 
            waveform_size.copy(), analog_probe_1.copy()
        ], ...]
        """
        # Divide for each channel
        CH0 = []
        CH1 = []
        
        self.send_feedback("Saving raw data as .dat file...")
        # Save raw data for debugging 
        for read in all_detect:
            #self.send_feedback(read)
            channel = str(read[0])
            flag = str(read[1])
            waveform_size = str(read[2])
            samples = read[3]
            
            struct = [channel, flag, waveform_size, samples]
            
            if struct[0] == '0': # CH0
                CH0.append(struct)
            elif struct[0] == '1': # CH1
                CH1.append(struct)
            else:
                self.send_feedback("Pulse was not in CH0 or CH1?!")
                self.send_feedback(read)
        
        #print(CH0)
        #print(CH1)
        
        self.save_raw_data(CH0.copy(), 'CH0')
        self.save_raw_data(CH1.copy(), 'CH1')
        
        self.send_feedback("Selecting valid pulses...")
        # Parse through data to find pulses + save to csv
        self.triage_data(CH0.copy(), 'CH0')
        self.triage_data(CH1.copy(), 'CH1')
        
        # Change dedicated graphs and lists
        try:
            self.send_feedback("Analysing CH0 pulses...")
            self.model_controller.analyse_data(
                self.view_controller.graph_showcase_ch0,
                self.get_ch0_analyser(),
                CH0
            )
        except IndexError: # There's no CH0 pulses
            self.send_feedback("There's no CH0 pulses!")
        except Exception as e:
            self.send_feedback(f"Unexpected error while saving CH0 ({e.__str__()}). Stopping program")
            raise e 
        
        try: 
            self.send_feedback("Analysing CH1 pulses...")
            self.model_controller.analyse_data(
                self.view_controller.graph_showcase_ch1,
                self.get_ch1_analyser(),
                CH1
            )
        except IndexError: # There's no CH0 pulses
            self.send_feedback("There's no CH1 pulses!")
        except Exception as e:
            self.send_feedback(f"Unexpected error while saving CH1 ({e.__str__()}). Stopping program")
            raise e
        
        # Save shoot parameters
        self.save_shoot_parameters()
        
        # Prepare for next shoot    
        self.send_feedback(f"Shoot finished! Check CH0 and CH1 tabs for results. Results are saved at '{self.path_of_shoot}'")
        self.increment_name_of_shoot()
        return
        
    """Functions for saving and loading parameters"""
    def generate_default_parameters(self):
        """
        Maps the name in the ParameterTreeviews (each tab) to the Controller's parameters
        TODO: This is where you add parameters if needed.
        NOTE: This is what the program uses to function properly (aka different parts of the 
        program talking to eachother).
        
        Some default values have been placed (From CoMPASS configuration).
        
        It uses the Parameter class to regroup all the information about a certain parameter.
        It makes it easier to change and access information about them accross the program.
        """
        # Tab 1 : Input
        self.input_parameters = {
            "Record Lenght (ns)": Parameter(
                "Record Lenght (ns)", ('15000','15000','15000'), "Set the length of the acquisition window (in ns)\nOnly uses board value.\nFrom 20 to 1310660\nIncrements of 20", 
                type='dig', dig_name='RECLEN', widget_type='entry', valide_range=(20,1310660)),
            "Pre-trigger (ns)": Parameter(
                "Pre-trigger (ns)", ('5000', '5000', '5000'), "Set the portion of the waveform acquisition window to be saved before the trigger (in ns)\nFrom 10 to 20440\nIncrements of 10",
                type='dig', dig_name='CH_PRETRG', widget_type='entry', valide_range=(10,20440)),
            "Polarity": Parameter(
                'Polarity', ('POLARITY_POSITIVE','POLARITY_POSITIVE','POLARITY_POSITIVE'), "Set the polarity (Negative/Positive) of the input signal to be processed by the DPP-PHA algorithm",
                type='dig', dig_name='CH_POLARITY', widget_type='combobox', choices=("POLARITY_POSITIVE", "POLARITY_NEGATIVE")),
            "N Sample baseline": Parameter(
                'N Sample baseline', ('BLINE_NSMEAN_32768','BLINE_NSMEAN_32768','BLINE_NSMEAN_32768'), "Set the number of samples used by the mean filter to calculate the input pulse baseline.\nFixed means that the baseline is not evaluated",
                type='dig', dig_name='CH_BLINE_NSMEAN', widget_type='combobox', choices=("BLINE_NSMEAN_FIXED", "BLINE_NSMEAN_16", "BLINE_NSMEAN_64", "BLINE_NSMEAN_256", "BLINE_NSMEAN_1024", "BLINE_NSMEAN_4096", "BLINE_NSMEAN_16384", "BLINE_NSMEAN_32768")),
            "DC Offset (%)": Parameter(
                "DC Offset (%)", ('5.0', '5.0','5.0'), "Allows the User to adjust the baseline position of the input signal on the ADC scale. The value is expressed in percentage of the input dynamic range.\nMoving the DC Offset corresponds to moving the baseline level of the input signal upward or downward in the dynamic scale to cover the full width of the pulse itself, thus avoiding saturation.\nFrom 0 to 100\nIncrements of 0.1",
                type='dig', dig_name='CH_DCOFFSET', widget_type='entry', valide_range=(0, 100)),
            "Coarse gain": Parameter(
                "Coarse gain",('COARSE_GAIN_X3','COARSE_GAIN_X3','COARSE_GAIN_X3'), "Allows to select the input dynamic range of each channel\nGain x1, x3, x10, x33 (corresponding to 10Vpp-3Vpp-1Vpp-0.3Vpp ranges)",
                type='dig', dig_name='CH_CGAIN', widget_type='combobox', choices=("COARSE_GAIN_X1", "COARSE_GAIN_X3", "COARSE_GAIN_X10", "COARSE_GAIN_X33")),
        }
        # Tab 2 : Discriminator
        self.discr_parameters = {
            'Threshold (lsb)': Parameter(
                'Threshold (lsb)', ('2000','2000','2000'), "Channel discriminator threshold\nThe units are in lsb (least significant bit)\n1 LSB = (Input dynamic range in Vpp)/2^(Nbit) [Volt]\nFrom 0 to 16383\nIncrements of 10",
                type='dig', dig_name='CH_THRESHOLD', widget_type='entry', valide_range=(0, 16383)),
            'Trigger holdoff (ns)': Parameter(
                'Trigger holdoff (ns)', ('480','480','480'), 'Set the Trigger Holdoff width\nDuring the Trigger Holdoff Time other trigger signals are not accepted by the digitizer\nFrom 10 to 655350\nIncrements of 10',
                type='dig', dig_name='CH_TRG_HOLDOFF', widget_type='entry', valide_range=(10, 655350)),
            'Fast discriminator smoothing': Parameter(
                'Fast discriminator smoothing', ('RCCR2_SMTH_1','RCCR2_SMTH_1','RCCR2_SMTH_1'), 'Defines the number of samples of a moving average filter used for the RC-CR2 signal formation\nThe RC-CR2 input signal second derivative smoothing value',
                type='dig', dig_name='CH_RCCR2_SMOOTH', widget_type='combobox', choices=("RCCR2_SMTH_1", "RCCR2_SMTH_2", "RCCR2_SMTH_4", "RCCR2_SMTH_8", "RCCR2_SMTH_16", "RCCR2_SMTH_32")),
            'Input rise time (ns)': Parameter(
                'Input rise time (ns)', ('200','200','200'), 'Value set to optimize the shape of the RC-CR2 signal used to trigger the board channels\nThis parameter defines the time constant of the derivative component of the PHA fast discriminator filter\nIn case of RC-CR2 this value must be equal (or 50% more) to the input rising edge, in such a way the RC-CR2 peak value corresponds to the height of the input signal.\nFrom 10 to 40950\nIncrements of 10',
                type='dig', dig_name='CH_RCCR2_RISE', widget_type='entry', valide_range=(10, 40950)),
        }
        # Tab 3 : Trapezoid
        self.trapezoid_parameters = {
            'Trap. rise time (ns)': Parameter(
                'Trap. rise time (ns)', ('5000','5000','5000'), 'Set the Trapezoid Rise Time\nFrom 10 to 40950\nIncrements of 10',
                type='dig', dig_name='CH_TRAP_TRISE', widget_type='entry', valide_range=(10,40950)),
            'Trap. flat top (ns)': Parameter(
                'Trap. flat top (ns)', ('1000','1000','1000'), 'Set the Trapezoid Flat Top width.\nFrom 10 to 40950\nIncrements of 10',
                type='dig', dig_name='CH_TRAP_TFLAT' ,widget_type='entry', valide_range=(10,40950)),
            'Trap. pole zero (ns)': Parameter(
                'Trap. pole zero (ns)', ('1000','1000','1000'), 'Set the Trapezoid Pole-Zero Cancellation. Must be set equal to the decay time of the preamplifier.\nFrom 10 to 655350\nIncrements of 10',
                type='dig', dig_name='CH_TDECAY', widget_type='entry', valide_range=(10,655350)),
            'Peaking time (%)': Parameter(
                'Peaking time (%)', ('80','80','80'), 'Position in percentage in the flat top region where the samples are used for the calculation of the peak height.\nThe peaking time is referred to the trigger position or to the trigger validation signal according to the trigger mode.\nIncrements of 0.1',
                type='dig', dig_name='CH_TRAP_FTD', widget_type='entry', valide_range=(0,100)),
            'N samples peak': Parameter(
                'N samples peak', ('PEAK_NSMEAN_1','PEAK_NSMEAN_1','PEAK_NSMEAN_1'), 'Corresponds to the number of samples for the averaging window of the trapezoid height calculation.\nNote: for a correct energy calculation the Peak Mean should be contained in the flat region of the Trapezoid Flat Top.',
                type='dig', dig_name='CH_PEAK_NSMEAN', widget_type='combobox', choices=('PEAK_NSMEAN_1', 'PEAK_NSMEAN_4', 'PEAK_NSMEAN_16', 'PEAK_NSMEAN_64')),
            'Peak holdoff (ns)': Parameter(
                'Peak holdoff (ns)', ('960','960','960'), 'The Peak Hold-off starts at the end of the trapezoid flat top and defines how close must be two trapezoids to be considered piled-up.\nZero is the case where the flat top of one trapezoid starts exactly at the end of the flat top of the previous one.\nFrom 80 to 81840\nOnly multiples of 8 are allowed',
                type='dig', dig_name='CH_PEAK_HOLDOFF', widget_type='entry', valide_range=(80,81840)),
            'Energy fine gain': Parameter(
                'Energy fine gain', ('1','1','1'), 'Allow the User to set the fine Gain.\nFrom 1 to 10\nIncrements of 0.01',
                type='dig', dig_name='CH_FGAIN', widget_type='entry', valide_range=(1,10)),
        }
        """ # Tab 4 : Spectra
        self.spectra_parameters = {
            
        } """
        # Tab -1 : Analyse
        self.analyse_parameters = {
            "Méthode du calcul d'aire": Parameter(
                "Méthode du calcul d'aire", 'trap', "'trap': Utilise la méthode des trapèzes\n'approx-HRM': Somme de toutes les points multipliée par dt (High Resolution Method)",
                type='FLASHy', widget_type='combobox', choices=('trap', 'approx-HRM')),
            "Méthode de mise à niveau": Parameter(
                "Méthode de mise à niveau", 'dynamic-median', "'median': Prend les 200 premiers points et utilise sa médianne pour mettre à zéro\n'dynamic-median': Calcule la dérivée du pulse pour trouver le début et la fin du pulse. Trouve la médianne des points hors-pulse et l'utilise pour mettre à zéro.\n'dynamic-mean':  Calcule la dérivée du pulse pour trouver le début et la fin du pulse. Trouve la moyenne des points hors-pulse et l'utilise pour mettre à zéro.",
                type='FLASHy', widget_type='combobox', choices=("median", "dynamic-mean", "dynamic-median")),
            "Graphique 1": Parameter(
                "Graphique 1", "Pulse", "Choix pour ce que le grahique 1 montre\nPulse: Affiche le voltage (en V) de chaque pulse selon le temps (en µs)\nAire: Affiche l'aire sous la courbe du pulse correspondant (en nC)",
                type='FLASHy', widget_type='combobox', choices=('Pulse', 'Aire')),
            "Graphique 2": Parameter(
                "Graphique 2", "Pulse", "Choix pour ce que le grahique 2 montre\nPulse: Affiche le voltage (en V) de chaque pulse selon le temps (en µs)\nAire: Affiche l'aire sous la courbe du pulse correspondant (en nC)",
                type='FLASHy', widget_type='combobox', choices=('Pulse', 'Aire')),
            "Facteur de conversion: [V*s] --> [C]": Parameter(
                "Facteur de conversion: [V*s] --> [C]", '1 / 33.33', "Permet de passer de V*s à C\nRemarque: Malgré le fait que les graphiques ne sont pas affichés avec ces unités, le facteur de conversion doit respecter l'équation",
                type='FLASHy', widget_type='entry'),
            "Facteur de conversion: [nC] --> [cGy]": Parameter(
                "Facteur de conversion: [nC] --> [cGy]", '2', "Permet de passer de nC à cGy\nRemarque: Malgré le fait que les graphiques ne sont pas affichés avec ces unités, le facteur de conversion doit respecter l'équation",
                type='FLASHy', widget_type='entry'),
        }

        self.parameters_tuple = (self.input_parameters, self.discr_parameters, self.trapezoid_parameters, self.analyse_parameters)
    def save_parameters(self, path:str='parameters.txt'):
        file_name_par = path
        with open(file_name_par, 'w') as f:
            header = 'Paramètres\n'
            
            input_par = ['Input:\n']
            for par in self.input_parameters.values():
                txt = '\t' + par.extract_parameter() + '\n'
                input_par.append(txt)
            discr_par = ['Discriminator:\n']
            for par in self.discr_parameters.values():
                txt = '\t' + par.extract_parameter() + '\n'
                discr_par.append(txt)
            trap_par = ['Trapezoid:\n']
            for par in self.trapezoid_parameters.values():
                txt = '\t' + par.extract_parameter() + '\n'
                trap_par.append(txt)
            analyse_par = ['Analyse:\n']
            for par in self.analyse_parameters.values():
                txt = '\t' + par.extract_parameter() + '\n'
                analyse_par.append(txt)
            
            f.write(header)
            f.writelines(input_par)
            f.writelines(discr_par)
            f.writelines(trap_par)
            f.writelines(analyse_par)
    def _safe_eval(self, value):
        try:
            return literal_eval(value)  # Safely parse literals like lists, dicts, and tuples
        except (ValueError, SyntaxError):
            return value  # Return as-is if not a literal
    def parse_data(self, file_path):
        """data = sections as keys and entries as lists of dicts"""
        data = defaultdict(list)
        
        with open(file_path, 'r') as file:
            content = file.read()
        
        # Split sections based on headers
        sections = re.split(r'^(?=\w+:)', content, flags=re.MULTILINE)
        
        for section in sections:
            if not section.strip():
                continue
            
            # Extract section header (e.g., Input, Discriminator)
            header_match = re.match(r'^(\w+):', section)
            if header_match:
                section_name = header_match.group(1)
            else:
                continue
            
            # Extract each parameter block
            params = re.findall(
                r"name=(.*?), values=(.*?), description=(.*?), type=(.*?), widget_type=(.*?), choices=(.*?), valide_range=(.*?), dig_name=(.*?)\n",
                section, flags=re.DOTALL
            )
            
            for param in params:
                data[section_name].append({
                    "name": param[0].strip(),
                    "values": self._safe_eval(param[1].strip()),
                    "description": param[2].replace(r"\\n", "\n").strip(),
                    "type": param[3].strip(),
                    "widget_type": param[4].strip(),
                    "choices": eval(param[5].strip()) if param[5].strip() != "None" else None,
                    "valide_range": eval(param[6].strip()) if param[6].strip() != "None" else None,
                    "dig_name": param[7].strip()
                })
        
        return data 
    def load_parameters_on_open(self):
        try:
            # Get info from file
            all_parameters = self.parse_data('parameters.txt')
            
            print('Loading parameters')
            
            input_par_dicts   = all_parameters.get('Input')
            discr_par_dicts   = all_parameters.get('Discriminator')
            trap_par_dicts    = all_parameters.get('Trapezoid')
            analyse_par_dicts = all_parameters.get('Analyse')
            
            input_par   : dict[str, Parameter] = {}
            discr_par   : dict[str, Parameter] = {}
            trap_par    : dict[str, Parameter] = {}
            analyse_par : dict[str, Parameter] = {}
            
            if input_par_dicts:
                for param in input_par_dicts:
                    input_par[param['name']] = Parameter(
                        name=param['name'], values=param['values'], description=param['description'], 
                        type=param['type'], dig_name=param['dig_name'], widget_type=param['widget_type'], 
                        choices=param['choices'], valide_range=param['valide_range']
                    )
            
            if discr_par_dicts:
                for param in discr_par_dicts:
                    discr_par[param['name']] = Parameter(
                        name=param['name'], values=param['values'], description=param['description'], 
                        type=param['type'], dig_name=param['dig_name'], widget_type=param['widget_type'], 
                        choices=param['choices'], valide_range=param['valide_range']
                    )
                    
            if trap_par_dicts:
                for param in trap_par_dicts:
                    trap_par[param['name']] = Parameter(
                        name=param['name'], values=param['values'], description=param['description'], 
                        type=param['type'], dig_name=param['dig_name'], widget_type=param['widget_type'], 
                        choices=param['choices'], valide_range=param['valide_range']
                    )
            
            if analyse_par_dicts:
                for param in analyse_par_dicts:
                    analyse_par[param['name']] = Parameter(
                        name=param['name'], values=param['values'], description=param['description'], 
                        type=param['type'], dig_name=param['dig_name'], widget_type=param['widget_type'], 
                        choices=param['choices'], valide_range=param['valide_range']
                    )
                    
            self.input_parameters     = input_par
            self.discr_parameters     = discr_par
            self.trapezoid_parameters = trap_par
            self.analyse_parameters   = analyse_par
            
            self.parameters_tuple = (self.input_parameters, self.discr_parameters, self.trapezoid_parameters, self.analyse_parameters)
            
        except FileNotFoundError: # The file doesn't exist
            print('Default parameters')
            self.generate_default_parameters()
    def save_shoot_parameters(self):
        # Create path to save to
        path = os.path.join(self.path_of_shoot, 'shoot_parameters.txt')
        self.save_parameters(path)  
    
    def generate_default_internal_parameters(self):
        # Variables for everything related to saving stuff
        time = datetime.now()
        date = fr"{time.day}-{time.month}-{time.year}"
        
        self.project_path     = 'DAQ'
        self.path_to_instance = os.path.join(self.project_path, f'open_on_{date}')
        self.increment        = 1
        self.name_of_shoot    = f'default'
        self.path_to_feedback = 'Feedback'
        self.incremented_name = 'default_1'
        self.path_of_shoot    = os.path.join(self.path_to_instance, self.incremented_name)
    def parse_internal_par(self, path):
        all_parameters = {}
        with open(path, 'r') as f:
            for line in f.readlines():
                split = line.strip('\n').split(';')
                all_parameters[split[0]] = split[1]
        return all_parameters     
    def load_internal_parameters_on_open(self):
        try:
            all_parameters = self.parse_internal_par('internal_parameters.txt')
            
            print("Loading internal parameters")
            
            time = datetime.now()
            date = fr"{time.day}-{time.month}-{time.year}"
            
            self.project_path     = all_parameters.get('project_path')
            self.path_to_instance = os.path.join(self.project_path, f'open_on_{date}')
            self.increment        = int(all_parameters.get('increment'))
            self.name_of_shoot    = all_parameters.get('name_of_shoot')
            self.path_to_feedback = all_parameters.get('path_to_feedback')
            self.incremented_name = all_parameters.get('incremented_name')
            self.path_of_shoot    = os.path.join(self.path_to_instance, self.incremented_name)
            
        except FileNotFoundError: # The internal parameter file doesn't exist
            print('Default internal parameters')
            self.generate_default_internal_parameters()
        
        try: 
            self.create_instance_directory()
            self.create_shoot_directory()
        except FileNotFoundError: # The project directory got deleted
            print("Can't find project directory, creating default")
            self.generate_default_internal_parameters()
            self.create_instance_directory()
            self.create_shoot_directory()
            
    def save_internal_parameters(self):
        file_name_par = 'internal_parameters.txt'
        with open(file_name_par, 'w') as f:
            f.write(f'project_path;{self.project_path}\n')
            f.write(f'increment;{self.increment}\n')
            f.write(f'name_of_shoot;{self.name_of_shoot}\n')
            f.write(f'path_to_feedback;{self.path_to_feedback}\n')
            f.write(f'incremented_name;{self.incremented_name}\n')
    def set_project_path(self):
        project_path = filedialog.askdirectory(
            title="Select path to save data to",
        )
        if not project_path:
            self.send_feedback("Please select a folder")
            return
        self.send_feedback(f"Saving project at '{project_path}'")

        time = datetime.now()
        date = fr"{time.day}-{time.month}-{time.year}"
        
        self.project_path     = project_path
        self.path_to_instance = os.path.join(self.project_path, f'open_on_{date}')
        #self.increment        = all_parameters.get('increment')
        #self.name_of_shoot    = all_parameters.get('name_of_shoot')
        self.path_to_feedback = os.path.join(self.project_path, "Feedback")
        #self.incremented_name = all_parameters.get('incremented_name')
        self.path_of_shoot    = os.path.join(self.path_to_instance, self.incremented_name)
        
        self.create_instance_directory()
        self.create_shoot_directory()
        
        # Change feedback
        self.view_controller.set_feedback_project_tag(project_path)
    
# Stores everything related to parameters
class Parameter:
    def __init__(self, name:str, values:Tuple[str,str,str] | str, description:str, type:Literal['dig', 'FLASHy'], widget_type:Literal['entry', 'combobox'], 
                 choices:tuple[str, ...]|None=None, valide_range: Tuple[float|int, float|int]|None=None, dig_name:str='default'):
        """Initialise the parameter.\n
        By default, everything is on the board (CH0 and CH1).\n
        If 'FLASHy' is set to True, then there's no digitizer shenanegans"""
        self.name = name
        self.description = description
        self.widget_type = widget_type
        self.choices = choices
        self.valide_range = valide_range
        self.dig_name = dig_name
        
        self.type = type
        if self.type == 'dig':
            self.state = 'board' # Possible states : ['board', 'CH0', 'CH1', 'default']
            self.row = [self.name, values[0], values[1], values[2]]
        else:
            self.state = 'choice'
            self.row = [self.name, values]
    
    # Channel logic
    def change_state(self, new_state:Literal['board', 'CH0', 'CH1', 'default']):
        if self.type == 'dig' and new_state in {'board', 'CH0', 'CH1', 'default'}: # Must be a digitizer parameter
            self.state = new_state
    
    def get_name(self) -> str:
        return self.name
    def get_description(self) -> str:
        return self.description
    def set_choices(self, choices:tuple[str, ...]):
        self.choices = choices
    def get_choices(self) -> tuple[str, ...] | None:
        return self.choices
    def set_valide_range(self, valide_range:Tuple[float|int, float|int]):
        self.valide_range = valide_range
    def get_valide_range(self) -> Tuple[float|int, float|int] | None:
        return self.valide_range
    def get_widget_type(self) -> str:
        return self.widget_type
    def get_row(self) -> list[str]:
        '''(name, value board, value CH0, value CH1)'''
        return self.row
    def set_row(self, value, index):
        self.row[index] = value
    def get_state(self) -> str:
        return self.state
    def get_parameter(self) -> List[str]:
        value = self.row[1:]
        value.append(self.state)
        return value
    def get_dig_name(self) -> str:
        return self.dig_name
            
    def extract_parameter(self) -> str:
        """self, name:str, value:str, description:str, type:Literal['dig', 'FLASHy'], widget_type:Literal['entry', 'combobox'], 
                 choices:tuple[str, ...]|None=None, valide_range: Tuple[float|int, float|int]|None=None, dig_name:str='default'):
        """
        if len(self.row) == 2:
            variables = {
                'name': self.name,
                'values': self.row[1],
                'description': self.description.replace('\n', r'\\n'),
                'type': self.type,
                'widget_type': self.widget_type,
                'choices': self.choices,
                'valide_range': self.valide_range,
                'dig_name': self.dig_name,
            }
            txt = ', '.join(f'{key}={value}' for key, value in variables.items())
        else:
            variables = {
                'name': self.name,
                'values': self.row[1:],
                'description': self.description.replace('\n', r'\\n'),
                'type': self.type,
                'widget_type': self.widget_type,
                'choices': self.choices,
                'valide_range': self.valide_range,
                'dig_name': self.dig_name,
            }
            txt = ', '.join(f'{key}={value}' for key, value in variables.items())
        return txt

    def __str__(self) -> str:
        return f"Name: {self.name}. State: {self.state}. Values: {self.row}"

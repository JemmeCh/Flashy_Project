from typing import Any, Dict, List, Literal, Tuple

from traitlets import default

from Controller.ModelController import ModelController
from Controller.ViewController import ViewController
from Model.DataAnalyser import DataAnalyser
from Model.Digitizer import Digitizer
from Model.Error import Error

# This class contains all the different settings of the program and
# is used as a link between the models and the views
class Controller():
    def __init__(self, view_controller:ViewController, model_controller:ModelController) -> None:
        self.view_controller = view_controller
        self.model_controller = model_controller
        self.error_handling = Error(self)

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
                "Record Lenght (ns)", '15000', "Set the length of the acquisition window (in ns)\nFrom 20 to 1310660\nIncrements of 20", 
                type='dig', dig_name='RECLEN', widget_type='entry', valide_range=(20,1310660)),
            "Pre-trigger (ns)": Parameter(
                "Pre-trigger (ns)", '5000', "Set the portion of the waveform acquisition window to be saved before the trigger (in ns)\nFrom 10 to 20440\nIncrements of 10",
                type='dig', dig_name='CH_PRETRG', widget_type='entry', valide_range=(10,20440)),
            "Polarity": Parameter(
                'Polarity', 'POLARITY_POSITIVE', "Set the polarity (Negative/Positive) of the input signal to be processed by the DPP-PHA algorithm",
                type='dig', dig_name='CH_POLARITY', widget_type='combobox', choices=("POLARITY_POSITIVE", "POLARITY_NEGATIVE")),
            "N Sample baseline": Parameter(
                'N Sample baseline', 'BLINE_NSMEAN_32768', "Set the number of samples used by the mean filter to calculate the input pulse baseline.\nFixed means that the baseline is not evaluated",
                type='dig', dig_name='CH_BLINE_NSMEAN', widget_type='combobox', choices=("BLINE_NSMEAN_FIXED", "BLINE_NSMEAN_16", "BLINE_NSMEAN_64", "BLINE_NSMEAN_256", "BLINE_NSMEAN_1024", "BLINE_NSMEAN_4096", "BLINE_NSMEAN_16384", "BLINE_NSMEAN_32768")),
            "DC Offset (%)": Parameter(
                "DC Offset (%)", '5.0', "Allows the User to adjust the baseline position of the input signal on the ADC scale. The value is expressed in percentage of the input dynamic range.\nMoving the DC Offset corresponds to moving the baseline level of the input signal upward or downward in the dynamic scale to cover the full width of the pulse itself, thus avoiding saturation.\nFrom 0 to 100\nIncrements of 0.1",
                type='dig', dig_name='CH_DCOFFSET', widget_type='entry', valide_range=(0, 100)),
            "Coarse gain": Parameter(
                "Coarse gain",'COARSE_GAIN_X3', "Allows to select the input dynamic range of each channel\nGain x1, x3, x10, x33 (corresponding to 10Vpp-3Vpp-1Vpp-0.3Vpp ranges)",
                type='dig', dig_name='CH_CGAIN', widget_type='combobox', choices=("COARSE_GAIN_X1", "COARSE_GAIN_X3", "COARSE_GAIN_X10", "COARSE_GAIN_X33")),
        }
        # Tab 2 : Discriminator
        self.discr_parameters = {
            'Threshold (lsb)': Parameter(
                'Threshold (lsb)', '2000', "Channel discriminator threshold\nThe units are in lsb (least significant bit)\n1 LSB = (Input dynamic range in Vpp)/2^(Nbit) [Volt]\nFrom 0 to 16383\nIncrements of 10",
                type='dig', dig_name='CH_THRESHOLD', widget_type='entry', valide_range=(0, 16383)),
            'Trigger holdoff (ns)': Parameter(
                'Trigger holdoff (ns)', '480', 'Set the Trigger Holdoff width\nDuring the Trigger Holdoff Time other trigger signals are not accepted by the digitizer\nFrom 10 to 655350\nIncrements of 10',
                type='dig', dig_name='CH_TRG_HOLDOFF', widget_type='entry', valide_range=(10, 655350)),
            'Fast discriminator smoothing': Parameter(
                'Fast discriminator smoothing', 'RCCR2_SMTH_1', 'Defines the number of samples of a moving average filter used for the RC-CR2 signal formation\nThe RC-CR2 input signal second derivative smoothing value',
                type='dig', dig_name='CH_RCCR2_SMOOTH', widget_type='combobox', choices=("RCCR2_SMTH_1", "RCCR2_SMTH_2", "RCCR2_SMTH_4", "RCCR2_SMTH_8", "RCCR2_SMTH_16", "RCCR2_SMTH_32")),
            'Input rise time (ns)': Parameter(
                'Input rise time (ns)', '200', 'Value set to optimize the shape of the RC-CR2 signal used to trigger the board channels\nThis parameter defines the time constant of the derivative component of the PHA fast discriminator filter\nIn case of RC-CR2 this value must be equal (or 50% more) to the input rising edge, in such a way the RC-CR2 peak value corresponds to the height of the input signal.\nFrom 10 to 40950\nIncrements of 10',
                type='dig', dig_name='CH_RCCR2_RISE', widget_type='entry', valide_range=(10, 40950)),
        }
        # Tab 3 : Trapezoid
        self.trapezoid_parameters = {
            'Trap. rise time (ns)': Parameter(
                'Trap. rise time (ns)', '5000', 'Set the Trapezoid Rise Time\nFrom 10 to 40950\nIncrements of 10',
                type='dig', dig_name='CH_TRAP_TRISE', widget_type='entry', valide_range=(10,40950)),
            'Trap. flat top (ns)': Parameter(
                'Trap. flat top (ns)', '1000', 'Set the Trapezoid Flat Top width.\nFrom 10 to 40950\nIncrements of 10',
                type='dig', dig_name='CH_TRAP_TFLAT' ,widget_type='entry', valide_range=(10,40950)),
            'Trap. pole zero (ns)': Parameter(
                'Trap. pole zero (ns)', '1000', 'Set the Trapezoid Pole-Zero Cancellation. Must be set equal to the decay time of the preamplifier.\nFrom 10 to 655350\nIncrements of 10',
                type='dig', dig_name='CH_TDECAY', widget_type='entry', valide_range=(10,655350)),
            'Peaking time (%)': Parameter(
                'Peaking time (%)', '80', 'Position in percentage in the flat top region where the samples are used for the calculation of the peak height.\nThe peaking time is referred to the trigger position or to the trigger validation signal according to the trigger mode.\nIncrements of 0.1',
                type='dig', dig_name='CH_TRAP_FTD', widget_type='entry', valide_range=(0,100)),
            'N samples peak': Parameter(
                'N samples peak', 'PEAK_NSMEAN_1', 'Corresponds to the number of samples for the averaging window of the trapezoid height calculation.\nNote: for a correct energy calculation the Peak Mean should be contained in the flat region of the Trapezoid Flat Top.',
                type='dig', dig_name='CH_PEAK_NSMEAN', widget_type='combobox', choices=('PEAK_NSMEAN_1', 'PEAK_NSMEAN_4', 'PEAK_NSMEAN_16', 'PEAK_NSMEAN_64')),
            'Peak holdoff (ns)': Parameter(
                'Peak holdoff (ns)', '960', 'The Peak Hold-off starts at the end of the trapezoid flat top and defines how close must be two trapezoids to be considered piled-up.\nZero is the case where the flat top of one trapezoid starts exactly at the end of the flat top of the previous one.\nFrom 80 to 81840\nOnly multiples of 8 are allowed',
                type='dig', dig_name='CH_PEAK_HOLDOFF', widget_type='entry', valide_range=(80,81840)),
            'Energy fine gain': Parameter(
                'Energy fine gain', '1', 'Allow the User to set the fine Gain.\nFrom 1 to 10\nIncrements of 0.01',
                type='dig', dig_name='CH_FGAIN', widget_type='entry', valide_range=(1,10)),
        }
        """ # Tab 4 : Spectra
        self.spectra_parameters = {
            
        } """
        # Tab -1 : Analyse
        self.analyse_parameters = {
            "Méthode du calcul d'aire": Parameter(
                "Méthode du calcul d'aire", 'trap', "'trap': Utilise la méthode des trapèzes\n'naif': Somme de toutes les points multipliée par dt (Utiliser seulement pour des hautes résolutions)",
                type='FLASHy', widget_type='combobox', choices=('trap', 'naif')),
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
        
        self.parameters_tuple = (self.input_parameters, self.discr_parameters, self.analyse_parameters)
        
        # Bool that determines the state of the program
        self.isCONNECTING_TO_DIG:bool = False
        self.isTAKING_DATA:bool = False
        self.isCHANGING_SETTINGS:bool = False
        self.isGETTING_BASIC_INFO: bool = False
        self.isRECORDING:bool = False
        
        self.hasDIGITIZERCONNECTED: bool = False
    
    # Getting information from the models
    def get_data_analyser(self) -> DataAnalyser:
        return self.model_controller.get_data_analyser()
    def get_digitizer(self) -> Digitizer:
        return self.model_controller.get_digitizer()
        
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
        self.isRECORDING = False
    
    # From models to views
    def send_feedback(self, message:str):
        self.view_controller.send_feedback(message)
    # TODO: Change these so its like send_feedback    
    def change_aqc_panel_message(self):
        self.view_controller.bypass.data_aqc_panel.status_text
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
    
# Stores everything related to parameters
class Parameter:
    def __init__(self, name:str, value:str, description:str, type:Literal['dig', 'FLASHy'], widget_type:Literal['entry', 'combobox'], 
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
            self.row = [self.name, value, value, value]
        else:
            self.row = [self.name, value]
    
    # Channel logic
    def change_state(self, new_state:Literal['board', 'CH0', 'CH1', 'default']):
        if self.type == 'dig' and new_state in {'board', 'CH0', 'CH1', 'default'}: # Must be a digitizer parameter
            self.state = new_state
    
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
        return self.row
    def set_row(self, value, index):
        self.row[index] = value
    def get_state(self) -> str:
        return self.state
        
    def __str__(self) -> str:
        return f"Name: {self.name}. Values: {self.row}, "
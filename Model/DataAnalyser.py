import csv
import numpy as np

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from Controller.ModelController import ModelController


class DataAnalyser:
    def __init__(self, model_controller:"ModelController"):
        # Contains the sample points for each pulse
        self.pulse_info:np.ndarray = np.arange(25)
        # Number of points in each pulse
        self.SAMPLE_SIZE:int = 0
        # Contains the area of each pulse
        self.area_under_curve = np.arange(25)
        # Contains the dose delivered by each pulse
        self.dose = np.arange(25)
        # The time axis where each point is associated to a sample point
        self.t_axis = np.arange(25)
        # The spacing in ns between each sample point
        self.dt = 0
        # The number of pulse taken
        self.nbr_of_pulse:int = 0
        # Facteur de calibration fourni par le fabricant
        self.convertion_factor:float = 1 / 33.33
        # The compiled data with the format [nbr_of_pulse, area_under_curve, dose]
        self.data = [[]]
        # For accessing the model model controller. Mostly for future use
        self.model_controller = model_controller
    
    def read_file(self, path):
        info = []

        with open(path, newline='') as f:
            reader = csv.reader(f, dialect='CoMPASS')
            # Skip header :
            # ['BOARD;CHANNEL;TIMETAG;ENERGY;CALIB_ENERGY;FLAGS;PROBE_CODE;SAMPLES']
            next(f)
            for row in reader:
                # Isolate SAMPLES
                row = np.array(row[7:], dtype=int)
                info.append(row)
        
        # Change the analyser's data
        self.pulse_info = np.array(info)
        # Notify the user
        self.model_controller.send_feedback("Data extracted from file")
        
        self.prep_data()
    
    def prep_data(self):
        # Set SAMPLE_SIZE
        self.SAMPLE_SIZE = np.shape(self.pulse_info)[1] # Find number of columns
        
        # Calculate t_axis and dt
        self.t_axis, self.dt = np.linspace(
            0, self.model_controller.get_rcd_len() / 1000, self.SAMPLE_SIZE, retstep=True)

        # Find the number of pulse
        self.nbr_of_pulse = np.shape(self.pulse_info)[0] # Find number of rows
    
    def level_data(self):
        choice = self.model_controller.get_LEVELING_METHOD()
        match choice:
            case 'median':
                self.median_method()
            case 'dynamic-mean':
                self.derivation_method(choice)
            case 'dynamic-median':
                self.derivation_method(choice)
            case _:
                self.derivation_method('dynamic-mean')
    
    def median_method(self):
        threshold = 8

        # Calculate de median of each pulse
        sous = np.median(self.pulse_info[:, :200], axis=1)
        # Bring values close to zero
        self.pulse_info = (self.pulse_info.T - sous).T
        # Bring value to zero if lower than threshold
        self.pulse_info[np.abs(self.pulse_info) < threshold] = 0
    
    def derivation_method(self, choice:str):
        # Derivation calculations
        left  = self.pulse_info[:,  :-1]
        right = self.pulse_info[:, 1:  ]
        
        # THIS IS VERY IMPORTANT (AND TOOK TOO LONG TO FIND)
        variation = 10 # Interval at which the digitizer samples data (ie 10 per nanoseconds)
        deriver = (right - left) / variation
        
        # Find the threshold of the derivative
        deriver_tr = deriver[np.arange(10), np.abs(self.pulse_info).min(axis=1).astype(int)]
        
        threshold = 1.0 # This is found manually
        dervier_mask = np.abs(deriver) > threshold
        left_bond  = np.argmax(dervier_mask, axis=1)
        right_bond = np.nanargmax(np.where(
            dervier_mask[::-1], np.arange(dervier_mask.shape[1]), np.nan)[::-1], axis=1)
        
        # Isolate the pulse and set its derivative to inf
        col_indices = np.arange(deriver.shape[1])
        # Create a mask by checking if the column indices fall within the left and right bonds
        mask = (col_indices >= left_bond[:, None]) & (col_indices < right_bond[:, None])
        deriver[mask] = np.inf
        
        # Find the baseline of each pulse using the derivative and the derivative threshold
        baseline_mask = np.logical_or(np.abs(deriver) != np.inf, np.abs(deriver) < deriver_tr[:, np.newaxis])
        pulse_info_mask = np.where(baseline_mask, self.pulse_info[:,:-1], np.nan) # Where theres the pulse peak, values are nan
        
        # Do mean or median
        match choice:
            case 'dynamic-mean':
                baselines = np.nanmean(pulse_info_mask, axis=1) # Mean excluding values set at nan
            case 'dynamic-median':
                baselines = np.nanmedian(pulse_info_mask, axis=1) # Mediane excluding values set at nan
            case _:
                baselines = np.nanmean(pulse_info_mask, axis=1)
        
        self.pulse_info = self.pulse_info - baselines[:, np.newaxis]
        # The pulse should be 0 around a certain threshold like original level_data
        tozero_threshold = 8
        self.pulse_info[np.abs(self.pulse_info) < tozero_threshold] = 0
             
    def calculate_area(self):
        # Choosing which calculation method to use
        choice = self.model_controller.get_AREA_CALCULATION_METHOD()
        match choice:
            case 'trap':
                self.trapezoid_area()
            case 'naif':
                self.naif_area()
            case _:
                self.trapezoid_area()
                
    # Trapezoid method with matrices
    def trapezoid_area(self):
        left  = self.pulse_info[:,  :-1]
        right = self.pulse_info[:, 1:  ]
        
        # Calculating the area under each trapezoid
        area = (left + right) * self.dt / 2
        
        self.area_under_curve = np.sum(area, axis=1)
        self.convert_Vs2nC()

        # Calculating the total area of all the pulses
        self.total_area = np.sum(self.area_under_curve)
        
    # Arthur's method: usefull if the resolution is high
    def naif_area(self):
        self.area_under_curve = np.sum(self.pulse_info, axis=1) * self.dt
        self.convert_Vs2nC()
        
        # Calculating the total area of all the pulses
        self.total_area = np.sum(self.area_under_curve)
    
    def convert_Vs2nC(self):
        self.area_under_curve *= self.convertion_factor * 0.1
    
    def calculate_dose(self):
        # Place holder conversion TODO #################################
        self.dose = self.area_under_curve * 2
        # Calculating the total dose
        self.total_dose = np.sum(self.dose)
        
    def prepare_list(self):
        # Packing data to be read by the List
        # Format: [[1,area1,dose1], [2,area2,dose2], ..., 
        # [self.nbr_of_pulse,area(self.nbr_of_pulse),dose(self.nbr_of_pulse)]]
        self.data = [[i + 1, area, dose] for i, (area, dose) in 
                     enumerate(zip(self.area_under_curve, self.dose))]

        # Adding the total label
        self.data.append(["Total", self.total_area, self.total_dose])
    
    def get_pulse_info(self) -> np.ndarray:
        return self.pulse_info
    def get_t_axis(self) -> np.ndarray:
        return self.t_axis
    def get_area_under_curve(self) -> np.ndarray:
        return self.area_under_curve
    def get_nbr_of_pulse(self) -> int:
        return self.nbr_of_pulse
    def get_data_list(self) -> list[list[Any]]:
        return self.data

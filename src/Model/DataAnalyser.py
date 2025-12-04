import csv
import numpy as np
import pickle
from datetime import datetime

from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from src.Controller.ModelController import ModelController
    from src.View.GraphShowcase import GraphShowcase


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
        # For accessing the model controller
        self.model_controller = model_controller
    
    def determine_dialect(self, path):
        with open(path, 'r') as file:
            first_line = file.readline()
            file.seek(0)
            try:
                dialect = csv.Sniffer().sniff(first_line)
                return dialect
            except csv.Error:
                csv.register_dialect("CoMPASS", delimiter=';')
                return csv.get_dialect("CoMPASS")
    
    def read_csv(self, path:str):
        info = []
        dialect = self.determine_dialect(path)
        
        if dialect.delimiter == ';':
            self.model_controller.send_feedback("CoMPASS csv detected!")
            with open(path, newline='') as f:
                # CoMPASS
                # ['BOARD;CHANNEL;TIMETAG;ENERGY;CALIB_ENERGY;FLAGS;PROBE_CODE;SAMPLES']
                reader = csv.reader(f, dialect=dialect)
                next(f)
                for row in reader:
                    # Isolate SAMPLES
                    row = np.array(row[7:], dtype=int)
                    info.append(row)
        elif dialect.delimiter == ',':
            self.model_controller.send_feedback("FLASHy csv detected!")
            # FlASHy
            # ['Channel,Flag,Waveform_size,Samples']
            with open(path, newline='') as f:
                reader = csv.reader(f, dialect=dialect)
                next(f)
                for row in reader:
                    # Isolate SAMPLES
                    samples_str:str = row[-1].replace('[', "").replace(']','')
                    samples = samples_str.split(",")
                    row = np.array(samples, dtype=int)
                    info.append(row)
        return info
    
    def read_raw(self, path:str):
        info = []
        file = open(path, 'rb')
        while True:
            try:
                new_pulse = pickle.load(file)
                info.append(new_pulse[-1])
            except Exception as e:
                break
        file.close()
        return info
    
    def clean_data(self, data):
        # The goal is to remove the data that doesn't have pulses
        # Using standard deviation and range
        pulse_std = np.std(data, axis=1)
        pulse_range = np.ptp(data, axis=1)
        
        # Defined threshold 
        std_thres = 10
        range_thres = 10
        
        valid_pulses = (pulse_std > std_thres) & (pulse_range > range_thres)
        
        return data[valid_pulses]
    
    def read_file(self, path:str):
        # Determine if its a .dat or .csv file
        if path.lower().endswith(".csv"):
            info = self.read_csv(path)
        elif path.lower().endswith(".dat"):
            self.model_controller.send_feedback("To be implemented")
            #info = self.read_raw(path)
            return False
        else: # File format can't be analysed
            self.model_controller.send_feedback("Not a .csv or .dat file!")
            return False
        
        if len(info) == 0: # Check if the array is empty
            self.model_controller.send_feedback("No data to analyse!")
            return False
        
        # Remove flat with noise data
        clean_info = self.clean_data(np.array(info))
        
        # Change the analyser's data
        self.pulse_info = np.array(clean_info)
        # Notify the user
        self.model_controller.send_feedback("Data extracted from file")
        
        self.prep_data()
        return True
    
    def prep_data(self):
        # Set SAMPLE_SIZE
        self.SAMPLE_SIZE = np.shape(self.pulse_info)[1] # Find number of columns
        
        # Calculate t_axis and dt
        # *0.001 pour [ns] --> [µs]
        self.t_axis, self.dt = np.linspace(
            0, int(self.model_controller.get_rcd_len()) * 0.001, self.SAMPLE_SIZE, retstep=True)

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
            case 'cummulative-sum':
                self.cumulative_sum()
            case _:
                self.derivation_method('dynamic-mean')
                
        # The pulses are not in V but in LSB (see documentation for details)
        self.convert_LSB2V()
    
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
        deriver_tr = deriver[np.arange(self.nbr_of_pulse), np.abs(self.pulse_info).min(axis=1).astype(int)]
        
        threshold = 5.0 # 2025-07-07: 1.0 -> 5.0 due to NaN slice
        dervier_mask = np.abs(deriver) > threshold
        try:
            left_bond  = np.argmax(dervier_mask, axis=1)
            right_bond = np.nanargmax(np.where(
                dervier_mask[::-1], np.arange(dervier_mask.shape[1]), np.nan)[::-1], axis=1)
        except ValueError as e: # For exception of type 'ValueError: All-NaN slice encountered'
            print(e)
            self.model_controller.send_feedback("Fallback to 'cummulative-sum' method")
            self.cumulative_sum()
            return
        except Exception as e:
            print(e)
            self.model_controller.send_feedback("Other error encountered... Saving data for debugging")
            self._save_data_on_error()
            self.model_controller.send_feedback("Fallback to 'cummulative-sum' method")
            self.cumulative_sum()
            return
        
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
        
        if any(np.isnan(baselines)):
            # TODO: Dynamically change threshold
            self.model_controller.send_feedback("Warning: NaN baseline detected during 'derivation_method'! Adjust 'threshold' in source code")
            print("Info on NaN baseline: \nAppears to level the pulse (and does so), but corrupts the data. This doesn't affect other calculations, but is not optimal. \nLeft as is for now, but will need a way to change 'threshold' in GUI")
        
        self.pulse_info = self.pulse_info - baselines[:, np.newaxis]

    def cumulative_sum(self):
        # Cumulative sum and its derivatives
        cum_signal = np.cumsum(self.pulse_info, axis=1)
        first_deriv = np.diff(cum_signal, axis=1)
        second_deriv = np.diff(first_deriv, axis=1)
        
        # Detect pulse regions
        threshold = 15.0
        change_mask = np.abs(second_deriv) > threshold
        
        left_bond = np.argmax(change_mask, axis=1)
        right_bond = change_mask.shape[1] - 1 - np.argmax(change_mask[:, ::-1], axis=1)
        
        # Mask pulse regions (set to NaN) in original data
        col_indices = np.arange(self.pulse_info.shape[1] - 2)
        pulse_mask = (col_indices >= left_bond[:, None]) & (col_indices <= right_bond[:, None])
        baseline_data = np.where(~pulse_mask, self.pulse_info[:, :-2], np.nan)
        
        # Compute baseline (mean of non-pulse regions)
        baselines = np.nanmean(baseline_data, axis=1)
        
        self.pulse_info = self.pulse_info - baselines[:, np.newaxis]

    def calculate_area(self):
        # Choosing which calculation method to use
        choice = self.model_controller.get_AREA_CALCULATION_METHOD()
        match choice:
            case 'trap':
                self.trapezoid_area()
            case 'approx-HRM':
                self.HRM_area()
            case _:
                self.trapezoid_area()
                
    # Trapezoid method with matrices
    def trapezoid_area(self):
        left  = self.pulse_info[:,  :-1]
        right = self.pulse_info[:, 1:  ]
        
        # Calculating the area under each trapezoid
        area = (left + right) * self.dt / 2
        
        self.area_under_curve = np.nansum(area, axis=1)
        self.convert_Vs2nC()

        # Calculating the total area of all the pulses
        self.total_area = np.nansum(self.area_under_curve)
        
    # Arthur's method: High Resolution Method Approximation
    def HRM_area(self):
        self.area_under_curve = np.nansum(self.pulse_info, axis=1) * self.dt
        self.convert_Vs2nC()
        
        # Calculating the total area of all the pulses
        self.total_area = np.nansum(self.area_under_curve)
    
    def convert_LSB2V(self):
        coarse_gain:float = self.model_controller.get_COARSEGAIN()
        adc_n_bits:int = self.model_controller.get_ADC_NBIT()
        convertion_factor = coarse_gain / (2 ** adc_n_bits)
        # [LSB] --> [V]
        self.pulse_info *= convertion_factor
    
    def convert_Vs2nC(self):
        # [V*µs] --> [V*s]
        self.area_under_curve *= (1e6**2)
        # [V*s] --> [C]
        self.area_under_curve *= self.convertion_factor
        # [C] --> [nC] 
        self.area_under_curve *= 1e-9
    
    def calculate_dose(self):
        # Get controller convertion factor
        convertion_factor:float = self.model_controller.get_dose_factor()
        self.dose = self.area_under_curve * convertion_factor
        # Calculating the total dose
        self.total_dose = np.nansum(self.dose)
        
    def prepare_list(self):
        # Packing data to be read by the List
        # Format: [[1,area1,dose1], [2,area2,dose2], ..., 
        # [self.nbr_of_pulse,area(self.nbr_of_pulse),dose(self.nbr_of_pulse)]]
        self.data = [[i + 1, area, dose] for i, (area, dose) in 
                     enumerate(zip(self.area_under_curve, self.dose))]

        # Adding the total label
        self.data.append(["Total", self.total_area, self.total_dose])
    
    def analyse_data(self, graph_showcase:"GraphShowcase", data):
        """
        data: contient toute les pulses avec mean > 2000
        [[
            channel.copy(), flags.copy(), 
            waveform_size.copy(), analog_probe_1.copy()
        ], ...]
        """
        # Extract the information we need
        self.SAMPLE_SIZE = int(data[0][2])
        raw_pulses = []
        for pulses_info in data:
            raw_pulses.append(pulses_info[3])
        # Clean data
        clean_pulses = self.clean_data(np.array(raw_pulses))
        self.pulse_info = clean_pulses
        # Calculate t_axis and dt
        self.t_axis, self.dt = np.linspace(
            0, int(self.model_controller.get_rcd_len()) / 1000, self.SAMPLE_SIZE, retstep=True)

        # Find the number of pulse
        self.nbr_of_pulse = np.shape(self.pulse_info)[0] # Find number of rows
        
        # Do the rest
        self.model_controller.send_feedback("Leveling data...")
        self.level_data()
        self.model_controller.send_feedback("Calculating areas under the curves...")
        self.calculate_area()
        self.model_controller.send_feedback("Calculating dosage...")
        self.calculate_dose()
        self.model_controller.send_feedback("Updating graphs et list...")
        self.prepare_list()
        graph_showcase.update_pulse_graph()
        graph_showcase.update_area_graph()
        graph_showcase.update_list()
        self.model_controller.send_feedback("Data analysed!")

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

    def _save_data_on_error(self):
        time = datetime.now()
        hour = f"{time:%H-%M-%S}"
        date = fr"{time.day}-{time.month}-{time.year}"
        file_name = f'data_{date}_{hour}.npy'
        np.save(f"Feedback/{file_name}", self.pulse_info)
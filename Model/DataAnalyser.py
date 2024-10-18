import csv
import numpy as np

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Controller.ModelController import ModelController



class DataAnalyser:
    def __init__(self, model_controller:"ModelController"):
        self.pulse_info:np.ndarray = np.arange(25)
        self.model_controller = model_controller
        self.area_under_curve = np.arange(25)
        self.dose = np.arange(25)
        self.t_axis = np.arange(25)
        self.dt = 0
        self.nbr_of_pulse:int = 0
        self.SAMPLE_SIZE:int = 0
        self.convertion_factor:float = 0.
    
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
        # Notify the user TODO
        self.model_controller.send_feedback("Data extracted from file")
        
        self.prep_data()
    
    # TODO: Change it so the 200 is dynamic
    # Test: works good on October 9
    def level_data(self):
        threshold = 8

        # Calculate de median of each pulse
        sous = np.median(self.pulse_info[:, :200], axis=1)
        # Bring values close to zero
        self.pulse_info = (self.pulse_info.T - sous).T
        # Bring value to zero if lower than threshold
        self.pulse_info[np.abs(self.pulse_info) < threshold] = 0
        
    # Trapezoid method with matrices
    def calculate_area(self):
        left = self.pulse_info[:,  :-1]
        right = self.pulse_info[:, 1:  ]
        
        # Creating the switch to check if we're below x=0
        #lswitch = left  >= 0
        #rswitch = right >= 0 
        #switch = ~(lswitch & rswitch)
    
        # Calculating the area under each trapezoid
        area = (left + right) * self.dt / 2
        
        self.area_under_curve = np.sum(area, axis=1)
        self.convert_Vs2nC()
    
    def convert_Vs2nC(self):
        # Facteur de calibration fourni par le fabricant
        self.convertion_factor = 1 / 33.33
        self.area_under_curve *= self.convertion_factor
    
    def prep_data(self):
        # Set SAMPLE_SIZE
        self.SAMPLE_SIZE = np.shape(self.pulse_info)[1] # Find number of columns
        
        # Calculate t_axis and dt TODO
        self.t_axis, self.dt = np.linspace(
            0, self.model_controller.get_rcd_len() / 1000, self.SAMPLE_SIZE, retstep=True)

        # Find the number of pulse
        self.nbr_of_pulse = np.shape(self.pulse_info)[0] # Find number of rows
    
    def get_pulse_info(self) -> np.ndarray:
        return self.pulse_info
    def get_t_axis(self) -> np.ndarray:
        return self.t_axis
    def get_area_under_curve(self) -> np.ndarray:
        return self.area_under_curve
    def get_nbr_of_pulse(self) -> int:
        return self.nbr_of_pulse

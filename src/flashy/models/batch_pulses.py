import numpy as np
import msgspec

class BatchPulses(msgspec.Struct):
    """
    Dataclass containg information about a batch of pulses.
    
    ### Inherits:
        `msgspec.Struct`
    """
    # Analysis options
    analysis_level_method: str
    analysis_area_calc_method: str
    analysis_nC2cGy_factor: float
    
    # Digitizer options
    digitizer_sampeling_period_ns: float
    digitizer_ADC2V_factor: float
    
    # Detector options
    detector_Vns2nC_factor: float
    
    # Data
    pulses: np.ndarray
    raw_valid_pulses: np.ndarray = np.array([[]])
    area_under_curves: np.ndarray = np.array([])
    doses: np.ndarray = np.array([])
    
    # Flags
    discard_flag: bool = False
    
    @property
    def has_pulses(self) -> bool:
        return self.pulses.size > 0
    
    def add_pulses(
        self,
        pulses: np.ndarray,
        raw_pulses: np.ndarray,
        areas: np.ndarray,
        doses: np.ndarray,
    ):
        """
        Append new pulses to the current `BatchPulses` instance.
        
        Args:
            pulses (np.ndarray): New leveled pulses to be appended.
            raw_pulses (np.ndarray): New raw values of the pulses to be appended.
            areas (np.ndarray): Area under the curve of the pulses to be appended.
            doses (np.ndarray): Doses of the pulses to be appended.
        """
        combined_pulses = np.append(self.pulses, pulses, axis=0)
        combined_raw_pulses = np.append(self.raw_valid_pulses, raw_pulses, axis=0)
        combined_areas = np.append(self.area_under_curves, areas)
        combined_doses = np.append(self.doses, doses)
        self.pulses = combined_pulses
        self.raw_valid_pulses = combined_raw_pulses
        self.area_under_curves = combined_areas
        self.doses = combined_doses
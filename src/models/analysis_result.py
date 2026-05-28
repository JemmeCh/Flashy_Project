import numpy as np
import msgspec

from typing import List

from src.models.data_config import ProcessingConfig
from src.models.batch_pulses import BatchPulses


class AnalysisResult(msgspec.Struct):
    pulse_batches: List[BatchPulses]
    config: ProcessingConfig



# OBSELETE
class ChannelAnalysisResult(msgspec.Struct):
    # Channel name
    channel_name: str
    
    # Contains the sample points for each pulse
    pulses: np.ndarray = np.array(25)
    # The number of pulse taken
    nbr_of_pulses: int = 0
    # Number of points in each pulse
    sample_size: int = 0
    # Contains the area of each pulse
    area_under_curves: np.ndarray = np.array(25)
    # Contains the dose delivered by each pulse
    pulse_doses: np.ndarray = np.array(25)
    
    # TODO: Verify if this is only useful to GUI
    
    # The time axis where each point is associated to a sample point
    t_axis: np.ndarray = np.array(25)
    # The spacing in ns between each sample point
    dt: float = 0.0
    
    
    
    # REMOVE: This is a fixed value given by the manifacturor
    # It should be in the Configuration model, accessed by the analysis_service.py 
    # conversion_factor: float = 1 / 33.33
    
    # REMOVE: This prepares the data to be sent to the result table
    # The presenter needs to pass the AnalysisResult instance to the correct view after
    #data: np.ndarray() The compiled data with the format [nbr_of_pulse, area_under_curve, dose]

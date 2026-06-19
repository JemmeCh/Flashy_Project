import numpy as np
import msgspec

class BatchPulses(msgspec.Struct):
    """
    Container holding a batch of processed and raw pulse data along with
    associated analysis results.
    
    :inherits: :py:class:`msgspec.Struct`
    """
    
    # =======================================================================
    # Analysis options
    # =======================================================================
    
    analysis_level_method: str
    """Method used for pulse level reconstruction or processing."""
    analysis_area_calc_method: str
    """Method used to compute pulse area under the curve."""
    analysis_nC2cGy_factor: float
    """Conversion factor from nC to cGy for dose calculation."""
    
    # =======================================================================
    # Digitizer options
    # =======================================================================
    
    digitizer_sampeling_period_ns: float
    """Sampling period of the digitizer in nanoseconds."""
    digitizer_ADC2V_factor: float
    """Conversion factor from ADC units to volts."""
    
    # =======================================================================
    # Detector options
    # =======================================================================
    
    detector_Vns2nC_factor: float
    """Conversion factor from V·ns to nC for detector response."""
    
    # =======================================================================
    # Data
    # =======================================================================
    
    pulses: np.ndarray
    """Processed pulse data (leveled or reconstructed signals)."""
    raw_valid_pulses: np.ndarray = np.array([[]])
    """Raw pulse data after validity filtering."""
    area_under_curves: np.ndarray = np.array([])
    """Computed area under each pulse curve."""
    doses: np.ndarray = np.array([])
    """Dose values computed from pulses."""
    
    # =======================================================================
    # Flags
    # =======================================================================
    
    discard_flag: bool = False
    """Flag indicating whether this batch should be ignored in analysis."""
    
    @property
    def has_pulses(self) -> bool:
        """
        Check whether the batch contains any pulses.
        
        :returns: True if at least one pulse is present.
        :rtype: bool
        """
        return self.pulses.size > 0
    
    def add_pulses(
        self,
        pulses: np.ndarray,
        raw_pulses: np.ndarray,
        areas: np.ndarray,
        doses: np.ndarray,
    ):
        """
        Append new pulse data to the current batch.
        
        All arrays are concatenated along their first axis (or flattened where
        appropriate).
        
        :param pulses: Processed pulses to append.
        :type pulses: np.ndarray
        
        :param raw_pulses: Raw pulse data to append.
        :type raw_pulses: np.ndarray
        
        :param areas: Pulse area values to append.
        :type areas: np.ndarray
        
        :param doses: Dose values to append.
        :type doses: np.ndarray
        
        :returns: None
        :rtype: None
        """
        combined_pulses = np.append(self.pulses, pulses, axis=0)
        combined_raw_pulses = np.append(self.raw_valid_pulses, raw_pulses, axis=0)
        combined_areas = np.append(self.area_under_curves, areas)
        combined_doses = np.append(self.doses, doses)
        self.pulses = combined_pulses
        self.raw_valid_pulses = combined_raw_pulses
        self.area_under_curves = combined_areas
        self.doses = combined_doses
import numpy as np
from flashy.models.batch_pulses import BatchPulses

class PulseProcessor:
    """
    Service responsible for processing batches of pulses. This service exposes the `process_pulses` 
    method used primarily by `AnalysisService`.
    """
    def process_pulses(self, batch: BatchPulses) -> BatchPulses:
        """
        Process a `BatchPulses` instance according to its configuration.
        
        If no valid pulse is detected by `_clean_data`, the original batch is returned unchanged.
        
        Processing pipeline:
            - Select valid pulses (ALL)
            - Send valid pulses to disk (ALL)
            - Level data (analysis-specific)
            - Convert LSB → V (digitizer-specific: gain & ADC resolution)
            - Compute area (analysis + digitizer sampling period)
            - Convert V·µs → nC (detector-specific calibration factor)
            - Convert nC → cGy (analysis-specific calibration factor)
        
        :param batch: Batch of pulses to process.
        :type batch: BatchPulses
        
        :returns: Processed batch containing analysed pulse results (or original batch if no valid pulses).
        :rtype: BatchPulses
        """
        # Select valid pulses
        valid = self._clean_data(batch.pulses)
        if valid.size == 0:
            batch.discard_flag = True
            return batch
        valid = valid.astype(dtype=np.float64, copy=False)
        
        # Level data
        levelled = self._level_data(valid, batch.analysis_level_method)
        
        # Convert LSB --> V
        v = levelled * batch.digitizer_ADC2V_factor
        
        # Calculate area
        area = self._calculate_area(v, batch.analysis_area_calc_method, batch.digitizer_sampeling_period_ns)
        
        # Convert V*mus --> nC
        area_nC = area * batch.detector_Vns2nC_factor
        
        # Convert nC --> cGy
        doses = area_nC * batch.analysis_nC2cGy_factor
        
        return BatchPulses(
            pulses=v,
            raw_valid_pulses=valid,
            area_under_curves=area_nC,
            doses=doses,
            analysis_level_method=batch.analysis_level_method,
            analysis_area_calc_method=batch.analysis_area_calc_method,
            analysis_nC2cGy_factor=batch.analysis_nC2cGy_factor,
            digitizer_sampeling_period_ns=batch.digitizer_sampeling_period_ns,
            digitizer_ADC2V_factor=batch.digitizer_ADC2V_factor,
            detector_Vns2nC_factor=batch.detector_Vns2nC_factor,
        )
    
    def _clean_data(self, pulses: np.ndarray) -> np.ndarray:
        # The goal is to remove the data that doesn't have pulses
        # Using standard deviation and range
        pulse_std = np.std(pulses, axis=1)
        pulse_range = np.ptp(pulses, axis=1)
        
        # Defined threshold 
        std_thres = 10
        range_thres = 10
        
        mask = (pulse_std > std_thres) & (pulse_range > range_thres)
        valid_pulses = pulses[mask]
        return valid_pulses
    
    def _level_data(self, pulses: np.ndarray, level_method: str) -> np.ndarray:
        match level_method:
            case 'median':
                lowered_pulses = self._median_method(pulses)
            case 'cummulative-sum':
                lowered_pulses = self._cumulative_sum(pulses)
            case 'dynamic-mean':
                lowered_pulses = self._derivation_method(pulses, level_method)
            case 'dynamic-median':
                lowered_pulses = self._derivation_method(pulses, level_method)
            case _:
                lowered_pulses = self._derivation_method(pulses, 'dynamic-mean')
        return lowered_pulses
    
    def _calculate_area(self, pulses: np.ndarray, area_calc_method: str, sampling_period_ns: float) -> np.ndarray:
        match area_calc_method:
            case 'trap':
                area_under_curves = self._trapezoid_area(pulses, sampling_period_ns)
            case 'approx-HRM':
                area_under_curves = self._high_resolution_method_area(pulses, sampling_period_ns)
            case _:
                area_under_curves = self._trapezoid_area(pulses, sampling_period_ns)
        return area_under_curves
    
    # =======================================================================
    # Leveling methods
    # =======================================================================
    
    def _median_method(self, pulses: np.ndarray) -> np.ndarray:
        threshold = 8
        
        # Calculate de median of each pulse
        start_median = np.median(pulses[:, :200], axis=1)
        # Bring values close to zero
        lowered_pulses = (pulses.T - start_median).T
        # Bring value to zero if lower than threshold
        lowered_pulses[np.abs(lowered_pulses) < threshold] = 0
        
        return lowered_pulses
    
    def _cumulative_sum(self, pulses: np.ndarray) -> np.ndarray:
        # Cumulative sum and its derivatives
        cum_signal = np.cumsum(pulses, axis=1)
        first_deriv = np.diff(cum_signal, axis=1)
        second_deriv = np.diff(first_deriv, axis=1)
        
        # Detect pulse regions
        threshold = 15.0
        change_mask = np.abs(second_deriv) > threshold
        
        left_bond = np.argmax(change_mask, axis=1)
        right_bond = change_mask.shape[1] - 1 - np.argmax(change_mask[:, ::-1], axis=1)
        
        # Mask pulse regions (set to NaN) in original data
        col_indices = np.arange(pulses.shape[1] - 2)
        pulse_mask = (col_indices >= left_bond[:, None]) & (col_indices <= right_bond[:, None])
        baseline_data = np.where(~pulse_mask, pulses[:, :-2], np.nan)
        
        # Compute baseline (mean of non-pulse regions)
        baselines = np.nanmean(baseline_data, axis=1)
        
        lowered_pulses = pulses - baselines[:, np.newaxis]
        return lowered_pulses
    
    def _derivation_method(self, pulses: np.ndarray, level_method:str) -> np.ndarray:
        # Derivation calculations
        left  = pulses[:,  :-1]
        right = pulses[:, 1:  ]
        
        # THIS IS VERY IMPORTANT (AND TOOK TOO LONG TO FIND)
        variation = 10 # Interval at which the digitizer samples data (ie 10 per nanoseconds)
        deriver = (right - left) / variation
        
        # Find the threshold of the derivative
        nbr_of_pulses = np.shape(pulses)[0]
        deriver_tr = deriver[np.arange(nbr_of_pulses), np.abs(pulses).min(axis=1).astype(int)]
        
        threshold = 5.0 # 2025-07-07: 1.0 -> 5.0 due to NaN slice
        dervier_mask = np.abs(deriver) > threshold
        # TODO: Bug fix + SIGNAL + Handle exceptions better
        try:
            left_bond  = np.argmax(dervier_mask, axis=1)
            right_bond = np.nanargmax(np.where(
                dervier_mask[::-1], np.arange(dervier_mask.shape[1]), np.nan)[::-1], axis=1)
        except ValueError as e: # For exception of type 'ValueError: All-NaN slice encountered'
            print(e)
            #self.model_controller.send_feedback("Fallback to 'cummulative-sum' method")
            lowered_pulses = self._cumulative_sum(pulses)
            return lowered_pulses
        except Exception as e:
            print(e)
            #self.model_controller.send_feedback("Other error encountered... Saving data for debugging")
            #self._save_data_on_error()
            #self.model_controller.send_feedback("Fallback to 'cummulative-sum' method")
            lowered_pulses = self._cumulative_sum(pulses)
            return lowered_pulses
        
        # Isolate the pulse and set its derivative to inf
        col_indices = np.arange(deriver.shape[1])
        # Create a mask by checking if the column indices fall within the left and right bonds
        mask = (col_indices >= left_bond[:, None]) & (col_indices < right_bond[:, None])
        deriver[mask] = np.inf
        
        # Find the baseline of each pulse using the derivative and the derivative threshold
        baseline_mask = np.logical_or(np.abs(deriver) != np.inf, np.abs(deriver) < deriver_tr[:, np.newaxis])
        pulse_info_mask = np.where(baseline_mask, pulses[:,:-1], np.nan) # Where theres the pulse peak, values are nan
        
        # Do mean or median
        match level_method:
            case 'dynamic-mean':
                baselines = np.nanmean(pulse_info_mask, axis=1) # Mean excluding values set at nan
            case 'dynamic-median':
                baselines = np.nanmedian(pulse_info_mask, axis=1) # Mediane excluding values set at nan
            case _:
                baselines = np.nanmean(pulse_info_mask, axis=1)
        
        if any(np.isnan(baselines)):
            # TODO: Dynamically change threshold + SIGNAL
            #self.model_controller.send_feedback("Warning: NaN baseline detected during 'derivation_method'! Adjust 'threshold' in source code")
            print("Info on NaN baseline: \nAppears to level the pulse (and does so), but corrupts the data. This doesn't affect other calculations, but is not optimal. \nLeft as is for now, but will need a way to change 'threshold' in GUI")
        
        lowered_pulses = pulses - baselines[:, np.newaxis]
        return lowered_pulses
    
    # =======================================================================
    # Area calculation methods
    # =======================================================================
    
    def _trapezoid_area(self, pulses: np.ndarray, sampling_period_ns: float) -> np.ndarray:
        left  = pulses[:,  :-1]
        right = pulses[:, 1:  ]
        
        # Calculating the area under each trapezoid
        area = (left + right) * sampling_period_ns / 2
        
        area_under_curves = np.nansum(area, axis=1)
        return area_under_curves
    
    def _high_resolution_method_area(self, pulses: np.ndarray, sampling_period_ns: float) -> np.ndarray:
        area_under_curves = np.nansum(pulses, axis=1) * sampling_period_ns
        return area_under_curves

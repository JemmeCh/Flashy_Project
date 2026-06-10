import numpy as np
from typing import Any, List

from flashy.models.processing_config import ProcessingConfig
from flashy.models.batch_pulses import BatchPulses

class Normalizer:
    def on_load_create_batch(
        self, 
        events: List[dict[str, Any]], 
        processing_config: ProcessingConfig, 
        channel_id: int
    ) -> BatchPulses:
        pulses_list = []
        for event in events:
            pulses_list.append(event['samples'])
        pulses = np.array(pulses_list)
        batch_pulses = BatchPulses(
            pulses=pulses,
            analysis_level_method=processing_config.analysis.get_value('level_method'),
            analysis_area_calc_method=processing_config.analysis.get_value('area_calc_method'),
            analysis_nC2cGy_factor=processing_config.analysis.get_value('nC2cGy_factor'),
            digitizer_sampeling_period_ns=processing_config.acquisition.digitizer.sampling_period_ns,
            digitizer_ADC2V_factor=processing_config.acquisition.digitizer.get_adc_to_volts_factor(channel_id),
            detector_Vns2nC_factor=processing_config.acquisition.detector_assignments[channel_id].detector.get_value('Vs2C_factor')
        )
        return batch_pulses
    
    def create_acquisition_result_batch(
        self,
        processing_config: ProcessingConfig,
        channel_id: int
    ) -> BatchPulses:
        reclen_ns = processing_config.acquisition.digitizer.channels[0].get_value('rdc_len')
        sampling_period_ns = processing_config.acquisition.digitizer.sampling_period_ns
        shape = (0, int(reclen_ns / sampling_period_ns))
        pulses = np.zeros(shape=shape)
        batch_pulses = BatchPulses(
            pulses=pulses,
            raw_valid_pulses=pulses,
            analysis_level_method=processing_config.analysis.get_value('level_method'),
            analysis_area_calc_method=processing_config.analysis.get_value('area_calc_method'),
            analysis_nC2cGy_factor=processing_config.analysis.get_value('nC2cGy_factor'),
            digitizer_sampeling_period_ns=processing_config.acquisition.digitizer.sampling_period_ns,
            digitizer_ADC2V_factor=processing_config.acquisition.digitizer.get_adc_to_volts_factor(channel_id),
            detector_Vns2nC_factor=processing_config.acquisition.detector_assignments[channel_id].detector.get_value('Vs2C_factor')
        )
        return batch_pulses
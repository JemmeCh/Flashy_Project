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
    
    def append_to_result_table(self, table_results: np.ndarray, table_batch: np.ndarray):
        results_shape = table_results.shape
        batch_shape = table_batch.shape
        
        max_row = np.max([results_shape[0], batch_shape[0]])
        max_col = np.max([results_shape[1], batch_shape[1]])
        max_size = (max_row, max_col) # Should be (N, 2)
        
        res = np.zeros(max_size)
        res[:table_results.shape[0], :] = table_results
        
        bat = np.zeros(max_size)
        bat[:table_batch.shape[0], :] = table_batch
        
        return np.append(res, bat, axis=1)



def main():
    from flashy.gui.widgets.result_panel_widget import ResultPanelWidget
    from flashy.services.analysis_service import AnalysisService
    from flashy.models.processing_config import AcquisitionConfig, ProcessingConfig
    from flashy.models.analysis.config import AnalysisConfig
    from flashy.models.analysis.result import AnalysisResult
    from flashy.digitizers.caen_dt5781.channel import CaenDT5781Channel
    from flashy.digitizers.caen_dt5781.config import CaenDT5781Config
    from flashy.detectors.detector import DetectorAssignment
    from flashy.detectors.bergoz_bct.bergoz_bct import BergozBCT
    
    from flashy.debug import make_test_data
    
    from PySide6.QtWidgets import QApplication
    
    t_bergoz = BergozBCT.create_default()
    t_caen_ch0 = CaenDT5781Channel.create_default(channel_id=0)
    t_caen_ch1 = CaenDT5781Channel.create_default(channel_id=1)
    t_analysis = AnalysisConfig.create_default()
    processing_config = ProcessingConfig(
        acquisition=AcquisitionConfig(
            digitizer=CaenDT5781Config(
                [t_caen_ch0, t_caen_ch1],
            ),
            detector_assignments=[
                DetectorAssignment(
                    detector=t_bergoz,
                    digitizer_channel=0
                    ),
                DetectorAssignment(
                    detector=t_bergoz,
                    digitizer_channel=1
                    ),
            ]
        ),
        analysis=t_analysis
    )
    test_data = make_test_data()
    analysis = AnalysisService()
    normalizer = Normalizer()
    
    nbr_of_channels = len(processing_config.acquisition.digitizer.channels)
    acquisition_results = []
    for i in range(nbr_of_channels):
        ch_batch = normalizer.create_acquisition_result_batch(
            processing_config=processing_config,
            channel_id=i
        )
        acquisition_results.append(ch_batch)
    acquisition_results: List[BatchPulses] = acquisition_results
    
    results = analysis.analyse_real_time(
        test_data,#type:ignore
        processing_config
    )
    
    for i, pulse_batch in enumerate(results.pulse_batches):
        if pulse_batch.has_pulses and not pulse_batch.discard_flag:
            change = True
            result_batch = acquisition_results[i]
            result_batch.add_pulses(
                pulse_batch.pulses,
                pulse_batch.raw_valid_pulses,
                pulse_batch.area_under_curves,
                pulse_batch.doses,
            )
            acquisition_results[i] = result_batch
    
    analysis_result = AnalysisResult(
            pulse_batches=acquisition_results,
            config=processing_config
        )
    
    app = QApplication()
    res_pan = ResultPanelWidget()
    res_pan.change_results(
        analysis_results=analysis_result
    )


if __name__ == '__main__':
    main()
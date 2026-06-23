import numpy as np
from typing import Any, List

from flashy.models.processing_config import AcquisitionConfig, ProcessingConfig
from flashy.models.analysis.config import AnalysisConfig
from flashy.models.user.config import UserConfig
from flashy.models.batch_pulses import BatchPulses
from flashy.services.logger.logger_service import get_logger

from flashy.detectors.detector import DetectorAssignment
from flashy.detectors.bergoz_bct.bergoz_bct import BergozBCT
from flashy.detectors.dummy.dummy import DummyDetector
from flashy.digitizers.caen_dt5781.channel import CaenDT5781Channel
from flashy.digitizers.caen_dt5781.config import CaenDT5781Config

# TODO:
# - Make confirmation methods support multiple detectors
# - Make confirmation methods support multiple digitizers
# - Make sure the number of channel correspond to the right number of detectors in config file


class Normalizer:
    def __init__(self) -> None:
        self._logger = get_logger()
    
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
    
    def confirm_user_config(self, user_config: "UserConfig") -> "UserConfig":
        defaults = UserConfig.create_default()
        good_config = UserConfig.create_default()
        for key, value in defaults.values.items():
            if key in user_config.values.keys():
                good_config.set_value(key, user_config.get_value(key))
            else:    
                self._logger.warning(f"Missing {key} parameter in JSON file. Adding default value")
                good_config.set_value(key, value)
        return good_config
    
    def confirm_processing_config(self, processing_config: "ProcessingConfig") -> "ProcessingConfig":
        # Digitizer
        if isinstance(processing_config.acquisition.digitizer, CaenDT5781Config):
            default_digitizer = self._make_default_caen_digitizer()
            good_digitizer= self._make_default_caen_digitizer()
        else:
            # TODO: Make dummy digitizer and dummy detectors for default
            default_digitizer = self._make_default_caen_digitizer()
            good_digitizer = self._make_default_caen_digitizer()
        
        for i, ch in enumerate(processing_config.acquisition.digitizer.channels):
            for key, value in ch.values.items():
                if key in processing_config.acquisition.digitizer.channels[i].values.keys():
                    good_digitizer.channels[i].set_value(
                        key, processing_config.acquisition.digitizer.channels[i].get_value(key)
                    )
                else:    
                    self._logger.warning(f"Missing {key} parameter in JSON file. Adding default value")
                    good_digitizer.channels[i].set_value(key, value)
        
        # Detector Assignment
        good_assignments = []
        for i in range(len(good_digitizer.channels)):
            cheking_detector = processing_config.acquisition.detector_assignments[i]
            if isinstance(cheking_detector.detector, BergozBCT):
                default_detector = self._make_bergoz_detector(i)
                good_detector = self._make_bergoz_detector(i)
            else:
                default_detector = self._make_default_detector(i)
                good_detector = self._make_default_detector(i)
            
            for key, value in default_detector.detector.values.items():
                if key in cheking_detector.detector.values.keys():
                    good_detector.detector.set_value(key, cheking_detector.detector.get_value(key))
                else:
                    self._logger.warning(f"Missing {key} parameter in JSON file. Adding default value")
                    good_detector.detector.set_value(key, value)
            good_assignments.append(good_detector)
        
        # Analysis
        default_analysis = AnalysisConfig.create_default()
        good_analysis = AnalysisConfig.create_default()
        
        for key, value in default_analysis.values.items():
            if key in processing_config.analysis.values.keys():
                good_analysis.set_value(key, processing_config.analysis.get_value(key))
            else:
                self._logger.warning(f"Missing {key} parameter in JSON file. Adding default value")
                good_analysis.set_value(key, value)
        
        good_config = ProcessingConfig(
            acquisition=AcquisitionConfig(
                digitizer=good_digitizer,
                detector_assignments=good_assignments
            ),
            analysis=good_analysis
        )
        return good_config
    
    def _make_default_caen_digitizer(self) -> CaenDT5781Config:
        t_caen_ch0 = CaenDT5781Channel.create_default()
        t_caen_ch1 = CaenDT5781Channel.create_default()
        digitizer_config = CaenDT5781Config(
            [t_caen_ch0, t_caen_ch1],
        )
        return digitizer_config
    
    def _make_bergoz_detector(self, i: int) -> DetectorAssignment:
        t_bergoz = BergozBCT.create_default()
        detector = DetectorAssignment(
            detector=t_bergoz
        )
        detector.detector.set_value('digitizer_channel', i)
        return detector
    
    def _make_default_detector(self, i: int) -> DetectorAssignment:
        t_detector = DummyDetector.create_default()
        detector = DetectorAssignment(
            detector=t_detector
        )
        detector.detector.set_value('digitizer_channel', i)
        return detector


def main():
    from flashy.models.analysis.result import AnalysisResult
    from flashy.digitizers.caen_dt5781.channel import CaenDT5781Channel
    from flashy.digitizers.caen_dt5781.config import CaenDT5781Config
    from flashy.gui.widgets.result_panel_widget import ResultPanelWidget
    from flashy.services.analysis_service import AnalysisService
    
    from flashy.debug import make_test_data
    
    from PySide6.QtWidgets import QApplication
    
    t_bergoz = BergozBCT.create_default()
    t_caen_ch0 = CaenDT5781Channel.create_default()
    t_caen_ch1 = CaenDT5781Channel.create_default()
    t_analysis = AnalysisConfig.create_default()
    processing_config = ProcessingConfig(
        acquisition=AcquisitionConfig(
            digitizer=CaenDT5781Config(
                [t_caen_ch0, t_caen_ch1],
            ),
            detector_assignments=[
                DetectorAssignment(
                    detector=t_bergoz
                    ),
                DetectorAssignment(
                    detector=t_bergoz
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
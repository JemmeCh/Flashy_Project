import numpy as np

from flashy.services.data_loader import DataLoader
from flashy.services.pulse_processor import PulseProcessor
from flashy.models.processing_config import ProcessingConfig
from flashy.models.analysis.result import AnalysisResult
from flashy.models.batch_pulses import BatchPulses

from typing import Any, List
from flashy.models.analysis.config import AnalysisConfig

class AnalysisService:
    """
    Service to analyse pulses in different formats.
    """
    def analyse_all_tdms_file(
        self, 
        filename: str, 
        analysis_config: "AnalysisConfig | None" = None
    ) -> AnalysisResult:
        """
        Analyse the data contained in a TDMS file.
        
        Args:
            path (str): Path to the TDMS file.
            analysis_config (AnalysisConfig | None, optional): Analysis configuration to use. Defaults to None (default configuration).
        
        Returns:
            AnalysisResult: Results of the analysis of the file's pulses using the chosen analysis configuration.
        """
        # Get file data
        data_loader = DataLoader()
        acquisition_config, file_analysis_config, data = data_loader.read_all_tdms_file(filename)
        
        # Choice of analysis configuration to be used for analysis
        if analysis_config:
            to_use_analysis_config = analysis_config
        else:
            to_use_analysis_config = file_analysis_config
        processing_config = ProcessingConfig(
            acquisition=acquisition_config,
            analysis=to_use_analysis_config
        )
        
        # Process BatchPulses for each channel
        result_list = []
        pulse_processor = PulseProcessor()
        for i, (_, events) in enumerate(data.items()):
            result = self._create_batch(events, processing_config, channel_id=i)
            batch_result = pulse_processor.process_pulses(result)
            result_list.append(batch_result)
        
        # Package results + return
        analysis_result = AnalysisResult(
            pulse_batches=result_list,
            config=processing_config
        )
        return analysis_result
    
    def analyse_real_time(
        self, 
        batch: list[np.ndarray], 
        processing_config: "ProcessingConfig"
    ) -> AnalysisResult:
        """
        Method used by `AnalysisWorker` for real-time pulse analysis.
        
        Args:
            batch (list[np.ndarray]): Unordered list of pulses to analyse.
            processing_config (ProcessingConfig): Current processing configuration
        
        Returns:
            result (AnalysisResult): Results of the analysis of the pulses.
        
        ### TODO:
        - Move 'order per channel' to future `Normalizer` class
        """
        # Order per channel
        data = {}
        for p in batch:
            # NOTE: Metadata is discarded
            channel_num = str(p[0])
            samples = p[-1]
            if channel_num not in data:
                data[channel_num] = []
            data[channel_num].append({
                'samples': samples
            })
        
        # Process BatchPulses for each channel
        result_list = []
        pulse_processor = PulseProcessor()
        for i, (_, events) in enumerate(data.items()):
            result = self._create_batch(events, processing_config, channel_id=i)
            batch_result = pulse_processor.process_pulses(result)
            result_list.append(batch_result)
        
        # Package results + return
        analysis_result = AnalysisResult(
            pulse_batches=result_list,
            config=processing_config
        )
        return analysis_result
    
    # =======================================================================
    # Helper methods
    # =======================================================================
    
    # TODO: Move to future Normalizer class
    def _create_batch(
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
    
    # =======================================================================
    # Legacy CSV file analyser
    # =======================================================================
    
    def legacy_analyse_csv_file(
        self, 
        path: str, 
        analysis_config: "AnalysisConfig | None" = None
    ) -> AnalysisResult | None:
        """
        Analyse the data contained in a CSV file using the default `ProcessingConfig`.\n
        WARNING: This works only for the Bergoz BCT with CeanDT5781 since it was exclusively used by FLASHy 1.0.
        
        Args:
            path (str): Path to the CSV file.
            analysis_config (AnalysisConfig | None, optional): Analysis configuration to use. Defaults to None (default configuration).
        
        Returns:
            result (AnalysisResult | None): Results of the analysis of the file's pulses using the chosen analysis configuration.
        ### TODO: 
        - Raise custom error
        """
        
        # Read Legacy CSV file
        data_loader = DataLoader()
        # TODO: Raise custom error
        from_file = data_loader.legacy_read_csv_file(path)
        if from_file is None:
            print("None was returned from DataLoader")
            return None
        acquisition_config, file_analysis_config, data = from_file
        
        # Choice of analysis configuration to be used for analysis
        if analysis_config:
            to_use_analysis_config = analysis_config
        else:
            to_use_analysis_config = file_analysis_config
        processing_config = ProcessingConfig(
            acquisition=acquisition_config,
            analysis=to_use_analysis_config
        )
        
        # Process BatchPulses for each channel
        result_list = []
        pulse_processor = PulseProcessor()
        for i, (_, events) in enumerate(data.items()):
            batch = self._create_batch(events, processing_config, channel_id=i)
            result_list.append(pulse_processor.process_pulses(batch))
        
        # Package results + return
        analysis_result = AnalysisResult(
            pulse_batches=result_list,
            config=processing_config
        )
        return analysis_result



def main():
    analysis_service = AnalysisService()
    
    # Test TDMS
    results = analysis_service.analyse_all_tdms_file('write_test.tdms')
    print(results.pulse_batches)
    
    # Test FLASHy 1.0
    """ results = analysis_service.legacy_analyse_csv_file('example_data/LEGACY-FLASHy1_0-pulses_2.csv')
    if results is None:
        print(f'result is {type(results)} type')
        return
    print(results.pulse_batches) """
    
    # Test CoMPASS 
    """ results = analysis_service.legacy_analyse_csv_file('example_data/LEGACY-CoMPASS-pulses_5.CSV')
    if results is None:
        print(f'result is {type(results)} type')
        return
    print(results.pulse_batches) """

if __name__ == '__main__':
    main()
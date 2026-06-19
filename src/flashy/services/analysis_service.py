import numpy as np

from flashy.services.data_loader import DataLoader
from flashy.services.pulse_processor import PulseProcessor
from flashy.models.processing_config import ProcessingConfig
from flashy.models.analysis.result import AnalysisResult
from flashy.services.normalizer import Normalizer
from flashy.services.logger.logger_service import get_logger

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flashy.models.analysis.config import AnalysisConfig

class AnalysisService:
    """
    Service to analyse pulses in different formats.
    """
    def __init__(self) -> None:
        self._normalizer = Normalizer()
        self._loader = DataLoader()
        self._processor = PulseProcessor()
        self._logger = get_logger()
    
    def analyse_file(
        self,
        filename: str,
        analysis_config: "AnalysisConfig | None" = None
    ) -> AnalysisResult:
        """
        Analyse data contained in a file. 
        
        Supported file types are the following:
        
        - ``.tdms``
        - ``.csv`` (legacy)
        
        .. warning::
        
            Legacy file types only work for the Bergoz BCT with CAEN DT5781,
            as it was exclusively used by FLASHy 1.0. They will use the default 
            acquisition and analysis configuration of FLASHy 1.0.
        
        :param filename: Path to the file.
        :type filename: str
        :param analysis_config: Analysis configuration to use. If None, a default configuration is used.
        :type analysis_config: AnalysisConfig | None, optional
        
        :returns: Results of the analysis of the file's pulses.
        :rtype: AnalysisResult
        """
        # Get file data
        try:
            acquisition_config, file_analysis_config, data = self._loader.read_file(filename)
        except Exception as e:
            raise e
        
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
        for i, (_, events) in enumerate(data.items()):
            batch = self._normalizer.on_load_create_batch(
                events, 
                processing_config, 
                channel_id=i
            )
            result_list.append(self._processor.process_pulses(batch))
        
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
        Perform real-time pulse analysis (used by `AnalysisWorker`).
        
        :param batch: Unordered list of pulses to analyse.
        :type batch: list[np.ndarray]
        :param processing_config: Current processing configuration.
        :type processing_config: ProcessingConfig
        
        :returns: Results of the analysis of the pulses.
        :rtype: AnalysisResult
        
        .. todo::
            - Move "order per channel" logic to a future `Normalizer` class
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
        for i, (_, events) in enumerate(data.items()):
            result = self._normalizer.on_load_create_batch(
                events, 
                processing_config, 
                channel_id=i
            )
            batch_result = self._processor.process_pulses(result)
            result_list.append(batch_result)
        
        # Package results + return
        analysis_result = AnalysisResult(
            pulse_batches=result_list,
            config=processing_config
        )
        return analysis_result


def main():
    """:meta private:"""
    analysis_service = AnalysisService()
    
    """ # Test error
    results = analysis_service.analyse_file('README.md') """
    
    # Test TDMS
    results = analysis_service.analyse_file('write_test.tdms')
    print(results.pulse_batches)
    
    # Test FLASHy 1.0
    """ results = analysis_service.analyse_file('example_data/LEGACY-FLASHy1_0-pulses_2.csv')
    if results is None:
        print(f'result is {type(results)} type')
        return
    print(results.pulse_batches) """
    
    # Test CoMPASS 
    """ results = analysis_service.analyse_file('example_data/LEGACY-CoMPASS-pulses_5.CSV')
    if results is None:
        print(f'result is {type(results)} type')
        return
    print(results.pulse_batches) """

if __name__ == '__main__':
    main()
import csv
import numpy as np
from nptdms import TdmsFile
import msgspec
import json

from typing import Any, List

from flashy.models.processing_config import AcquisitionConfig, ProcessingConfig
from flashy.models.analysis.config import AnalysisConfig
from flashy.models.user.config import UserConfig
from flashy.detectors.detector import DetectorAssignment
from flashy.services.logger.logger_service import get_logger

# TODO: 
# - In read_file: needs to check which channel it is for correct rdc_len (recent: what is blud talking about?)

class DataLoader:
    """
    Service for reading data files and returning parsed content.
    
    The methods of this class return an `AcquisitionConfig` and an `AnalysisConfig`
    (except legacy CSV reading), with data separated per channel. This allows the
    `AnalysisService` to construct a `ProcessingConfig` from these components or
    use a user-provided analysis configuration.
    """
    def __init__(self) -> None:
        self._logger = get_logger()
    
    def read_file(self, filename: str) -> tuple[AcquisitionConfig, AnalysisConfig, dict[str, List[dict[str, Any]]]]:
        if filename.lower().endswith('.tdms'):
            result = self.read_all_tdms_file(filename)
        elif filename.lower().endswith(".csv"):
            result = self.legacy_read_csv_file(filename)
        else: # File format can't be analysed
            raise NotImplementedError("This file type is not supported.")
        return result
    
    # =======================================================================
    # Read TDMS files
    # =======================================================================
    
    def read_all_tdms_file(self, filename: str) -> tuple[AcquisitionConfig, AnalysisConfig, dict[str, List[dict[str, Any]]]]:
        """
        Read a TDMS file and return its contents.
        
        :param filename: Path to the TDMS file.
        :type filename: str
        
        :returns: A tuple containing:
                    - Acquisition configuration used when saving
                    - Analysis configuration used when saving
                    - Dictionary of channel data
        :rtype: tuple[AcquisitionConfig, AnalysisConfig, dict[str, List[dict[str, Any]]]]
        """
        tdms_file = TdmsFile.read(filename)
        
        # Get acquisition configuration + used analysis configuration
        props = tdms_file.properties
        processing_config_json = json.loads(props['processing_config']) #type:ignore --> Tested and worked
        acquisition_config = msgspec.convert(processing_config_json['acquisition'], type=AcquisitionConfig)
        analysis_config = msgspec.convert(processing_config_json['analysis'], type=AnalysisConfig)
        
        # Get data per channel
        data = {}
        for group in tdms_file.groups():
            if group.name not in data:
                data[group.name] = []
            for channel in group.channels():
                data[group.name].append({
                    "channel": channel.name,
                    "samples": channel[:].astype(dtype=np.float64),
                    "properties": channel.properties
                })
        
        return (acquisition_config, analysis_config, data)
    
    def read_partial_tdms_file(self):
        """:meta private:"""
        # NOTE: If file is too big to load into memory, implement this
        pass
    
    # =======================================================================
    # Read configuration
    # =======================================================================
    
    def read_config_json_file(self) -> tuple[UserConfig, ProcessingConfig]:
        """
        Read the configuration file generated when the program was previously closed (`config.json`).
        
        :returns: Previously saved user and processing configuration.
        :rtype: tuple[UserConfig, ProcessingConfig]
        """
        filename_json: str = 'config.json'
        
        with open(filename_json, 'r') as f:
            all_dict: dict = json.load(f)
        user_config_dict = all_dict['user_config']
        processing_config_dict = all_dict['processing_config']
        user_config = msgspec.convert(user_config_dict, type=UserConfig)
        processing_config = msgspec.convert(processing_config_dict, type=ProcessingConfig)
        # TODO: Verify that the data is valid
        return user_config, processing_config
    
    # =======================================================================
    # Legacy CSV file reader
    # =======================================================================
    
    def legacy_read_csv_file(self, path: str) -> tuple[AcquisitionConfig, AnalysisConfig, dict[str, List[dict[str, Any]]]]:
        """
        Read a legacy CSV file from past shoots using the default FLASHy 1.0 configuration.
        
        .. warning::
        
            This method is legacy and only works for the Bergoz BCT with CAEN DT5781,
            as it was exclusively used by FLASHy 1.0.
        
        :param path: Path to the CSV file.
        :type path: str
        
        :returns: A tuple containing:
                    - Acquisition configuration (default FLASHy 1.0)
                    - Analysis configuration (default FLASHy 1.0)
                    - Dictionary containing pulse data per channel
        :rtype: tuple[AcquisitionConfig, AnalysisConfig, dict[str, List[dict[str, Any]]]]
        
        .. todo::
            - Add debugging/feedback signals
        """
        from flashy.digitizers.caen_dt5781.config import CaenDT5781Config 
        from flashy.digitizers.caen_dt5781.channel import CaenDT5781Channel
        from flashy.detectors.bergoz_bct.bergoz_bct import BergozBCT
        
        info = self._legacy_read_csv(path)
        if len(info) == 0: # Check if the array is empty
            # TODO: SIGNAL
            # self.model_controller.send_feedback("No data to analyse!")
            raise ValueError("No data to analyse!")
        
        # Format pulses into standard
        data = self._legacy_format_pulses(info)
        
        # Make default processing config
        acquisition_config = AcquisitionConfig(
            digitizer=CaenDT5781Config(
                [CaenDT5781Channel.create_default(channel_id=0)],
            ),
            detector_assignments=[
                DetectorAssignment(
                    detector=BergozBCT.create_default(),
                    digitizer_channel=0
                    )
                ]
        )
        analysis_config = AnalysisConfig.create_default()
        
        return acquisition_config, analysis_config, data
    
    def _legacy_determine_dialect(self, path):
        with open(path, 'r') as file:
            first_line = file.readline()
            file.seek(0)
            try:
                dialect = csv.Sniffer().sniff(first_line)
                return dialect
            except csv.Error:
                csv.register_dialect("CoMPASS", delimiter=';')
                return csv.get_dialect("CoMPASS")
    
    def _legacy_read_csv(self, path: str) -> list[np.ndarray]:
        info: list[np.ndarray] = []
        dialect = self._legacy_determine_dialect(path)
        
        if dialect.delimiter == ';':
            self._logger.info("CoMPASS csv detected!")
            with open(path, newline='') as f:
                # CoMPASS
                # ['BOARD;CHANNEL;TIMETAG;ENERGY;CALIB_ENERGY;FLAGS;PROBE_CODE;SAMPLES']
                reader = csv.reader(f, dialect=dialect)
                next(f)
                for row in reader:
                    # Isolate SAMPLES
                    row = np.array(row[7:], dtype=int)
                    info.append(row)
        elif dialect.delimiter == ',':
            self._logger.info("FLASHy csv detected!")
            # FlASHy
            # ['Channel,Flag,Waveform_size,Samples']
            with open(path, newline='') as f:
                reader = csv.reader(f, dialect=dialect)
                next(f)
                for row in reader:
                    # Isolate SAMPLES
                    samples_str: str = row[-1].replace('[', "").replace(']','')
                    samples = samples_str.split(",")
                    row = np.array(samples, dtype=int)
                    info.append(row)
        return info
    
    def _legacy_format_pulses(self, pulses: list[np.ndarray]) -> dict[str, List[dict[str, Any]]]:
        data = {
            '0': []
        }
        for i, pulse in enumerate(pulses):
            data['0'].append({
                'channel': f"Event_{i}",
                'samples': pulse.astype(dtype=np.float64),
                'properties': {}
            })
        return data


def main():
    """:meta private:"""
    path = 'write_test.tdms'
    data_loader = DataLoader()
    acquisition_config, analysis_config, data = data_loader.read_all_tdms_file(path)
    #print(data['CH0'][0]['properties'])
    #print(analysis_config)
    #print(acquisition_config)
    #for thing, thing2 in data.items():
    #    print(thing)
    #    print(thing2)
    #print(acquisition_config.digitizer.channels[0].coarse_gain)
    #print(type(acquisition_config.digitizer.channels[0].coarse_gain))
    #print(acquisition_config.digitizer.channels[0].get_field_value('coarse_gain'))
    #print(type(acquisition_config.digitizer.channels[0].get_field_value('coarse_gain')))
    
    user_config, processing_config = data_loader.read_config_json_file()
    print(user_config)
    print(processing_config)

if __name__ == "__main__":
    main()
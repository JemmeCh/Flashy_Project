import csv
import numpy as np
from nptdms import TdmsFile
import msgspec
import json

from typing import Any, List

from src.models.processing_config import AcquisitionConfig
from src.models.analysis.config import AnalysisConfig
from src.models.user_config import UserConfig
from src.detectors.detector import DetectorAssignment

# TODO: 
# - In read_file: needs to check which channel it is for correct rdc_len (recent: what is blud talking about?)
# - Raise errors instead of returning None

"""
THE FUNCTIONS OF THIS CLASS SHOULD RETURN AN AcquisitionConfig INSTANCE AND AN AnalysisConfig
WITH THE DATA SEPERATED PER CHANNEL (except old csv reading)!
THAT WAY, AnalysisService CAN CONSTRUCT A ProcessingConfig WITH THOSE TWO OR USE ANOTHER
AnalysisConfig SPECIFIED BY THE USER
"""


class DataLoader(object):
    # =======================================================================
    # Read TDMS files
    # =======================================================================
    
    def read_all_tdms_file(self, filename: str) -> tuple[AcquisitionConfig, AnalysisConfig, dict[str, List[dict[str, Any]]]]:
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
        # NOTE: If file is too big to load into memory, implement this
        pass
    
    # =======================================================================
    # Read user configuration
    # =======================================================================
    
    # TODO: add the previous config when program was closed (see objectifs)
    def read_user_config_json_file(self) -> UserConfig:
        filename_json: str = 'user_config.json'
        with open(filename_json, 'r') as f:
            user_config_json = json.load(f)
        user_config_json = json.loads(user_config_json)
        user_config = msgspec.convert(user_config_json, type=UserConfig)
        return user_config
    
    # =======================================================================
    # Legacy CSV file reader
    # =======================================================================
    
    def legacy_read_csv_file(self, path: str) -> tuple[AcquisitionConfig, AnalysisConfig, dict[str, List[dict[str, Any]]]] | None:
        """Read a legacy CSV file from past shoots using default configuration (FLASHy 1.0)"""
        from src.digitizers.caen_dt5781.config import CaenDT5781Config 
        from src.digitizers.caen_dt5781.channel import CaenDT5781Channel
        from src.detectors.bergoz_bct.bergoz_bct import BergozBCT
        
        # Determine if its .csv file
        if path.lower().endswith(".csv"):
            info = self._legacy_read_csv(path)
        else: # File format can't be analysed
            # TODO: SIGNAL
            # self.model_controller.send_feedback("Not a .csv or .dat file!")
            print("Not a .csv or .dat file!")
            # TODO: Raise custom error
            return None
        if len(info) == 0: # Check if the array is empty
            # TODO: SIGNAL
            # self.model_controller.send_feedback("No data to analyse!")
            print("No data to analyse!")
            # TODO: Raise custom error
            return None
        
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
    
    # TODO: SIGNALS..?
    def _legacy_read_csv(self, path: str) -> list[np.ndarray]:
        info: list[np.ndarray] = []
        dialect = self._legacy_determine_dialect(path)
        
        if dialect.delimiter == ';':
            # TODO: SIGNAL
            # self.model_controller.send_feedback("CoMPASS csv detected!")
            print("CoMPASS csv detected!")
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
            # TODO: SIGNAL
            # self.model_controller.send_feedback("FLASHy csv detected!")
            print("FLASHy csv detected!")
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
    
    #user_config = data_loader.read_user_config_json_file()
    #print(user_config)

if __name__ == "__main__":
    main()
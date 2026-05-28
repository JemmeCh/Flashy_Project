import msgspec
from typing import Literal

from src.digitizers.caen_dt5781.channel import CaenDT5781Channel

class CaenDT5781Config(msgspec.Struct):
    channels: list[CaenDT5781Channel]
    type: Literal['caen_dt5781'] = 'caen_dt5781'
    
    name: str = 'DT5781A'
    familycode: str = 'XX781'
    fw_type: str = 'DPP-PHA'
    serial_num: int = 27916
    max_rawdata_size: float = 1573904.0
    adc_nbits: int = 14
    adc_samplrate_msps: float = 100.0
    
    
    @property
    def sampling_period_ns(self) -> float:
        return 1e3 / self.adc_samplrate_msps
    
    
    def get_adc_to_volts_factor(self, channel_id: int) -> float:
        channel = self.channels[channel_id]
        convertion_factor = channel.coarse_gain / (2**self.adc_nbits)
        return convertion_factor
    
    # NOTE: Is this useful? why not digitizer.channels[0].coarse_gain = value ?
    def change_coarse_gain(self, value: Literal['10.0', '3.0', '1.0', '0.3'], channel_id: int) -> None:
        channel = self.channels[channel_id]
        channel.coarse_gain = float(value)

import msgspec
from typing import Literal

from flashy.digitizers.caen_dt5781.channel import CaenDT5781Channel

class CaenDT5781Config(msgspec.Struct):
    """
    Configuration for the Caen DT5781 digitizer.
    
    :inherits: :py:class:`msgspec.Struct`
    """
    channels: list[CaenDT5781Channel]
    """List of channel configurations."""
    type: Literal['caen_dt5781'] = 'caen_dt5781'
    """Fixed identifier of this digitizer."""
    name: str = 'DT5781A'
    """Human-readable device name."""
    familycode: str = 'XX781'
    """Hardware family code."""
    fw_type: str = 'DPP-PHA'
    """Firmware type."""
    serial_num: int = 27916
    """Device serial number."""
    max_rawdata_size: float = 1573904.0
    """Maximum raw data size in bytes."""
    adc_nbits: int = 14
    """ADC resolution in bits."""
    adc_samplrate_msps: float = 100.0
    """ADC sampling rate in MSPS."""
    
    
    @property
    def sampling_period_ns(self) -> float:
        """
        Sampling period in nanoseconds.
        
        :returns: Sampling period computed from ADC sampling rate.
        :rtype: float
        """
        return 1e3 / self.adc_samplrate_msps
    
    def get_adc_to_volts_factor(self, channel_id: int) -> float:
        """
        Compute ADC-to-volts conversion factor for a channel.
        
        :param channel_id: Index of the channel.
        :type channel_id: int
        
        :returns: Conversion factor based on coarse gain and ADC resolution.
        :rtype: float
        """
        channel = self.channels[channel_id]
        convertion_factor = channel.get_value('coarse_gain') / (2**self.adc_nbits)
        return convertion_factor
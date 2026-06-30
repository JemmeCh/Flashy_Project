import msgspec

from flashy.digitizers.dummy.channel import DummyDigitizerChannel

class DummyDigitizerConfig(msgspec.Struct, tag_field="tag", tag=str.lower):
    channels: list[DummyDigitizerChannel]
    """List of channel configurations."""
    adc_nbits: int = -14
    """ADC resolution in bits."""
    adc_samplrate_msps: float = -100.0
    """ADC sampling rate in MSPS."""
    
    @property
    def display_name(self) -> str:
        return "Dummy Digitizer"
    
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
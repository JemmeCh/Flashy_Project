import msgspec

class DigitizerChannel(msgspec.Struct):
    def get_adc_to_volts_factor(self, channel_id: int) -> float:
        ...
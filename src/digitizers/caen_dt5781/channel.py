from typing import ClassVar

from src.digitizers.digitizer_channel import DigitizerChannel
from src.digitizers.caen_dt5781.parameter_definition import CaenDT5781ParameterDefinition

class CaenDT5781Channel(DigitizerChannel):
    # Definitions
    DEFINITIONS = {
        # Input
        "rdc_len": CaenDT5781ParameterDefinition(
            name="Record Lenght (ns)",
            description="Set the length of the acquisition window (in ns)\nOnly uses board value.\nFrom 20 to 1310660\nIncrements of 20",
            widget_type="entry",
            choices=None,
            valid_range=(20, 1310660),
            digitizer_name="RECLEN",
        ),
        "pre_trig": CaenDT5781ParameterDefinition(
            name="Pre-trigger (ns)",
            description="Set the portion of the waveform acquisition window to be saved before the trigger (in ns)\nFrom 10 to 20440\nIncrements of 10",
            widget_type="entry",
            choices=None,
            valid_range=(10, 20440),
            digitizer_name="CH_PRETRG",
        ),
        "polarity": CaenDT5781ParameterDefinition(
            name="Polarity",
            description="Set the polarity (Negative/Positive) of the input signal to be processed by the DPP-PHA algorithm",
            widget_type="combobox",
            choices=("POLARITY_POSITIVE", "POLARITY_NEGATIVE"),
            valid_range=None,
            digitizer_name="CH_POLARITY",
        ),
        "sample_baseline": CaenDT5781ParameterDefinition(
            name="N Sample baseline",
            description="Set the number of samples used by the mean filter to calculate the input pulse baseline.\nFixed means that the baseline is not evaluated",
            widget_type="combobox",
            choices=(
                "BLINE_NSMEAN_FIXED",
                "BLINE_NSMEAN_16",
                "BLINE_NSMEAN_64",
                "BLINE_NSMEAN_256",
                "BLINE_NSMEAN_1024",
                "BLINE_NSMEAN_4096",
                "BLINE_NSMEAN_16384",
                "BLINE_NSMEAN_32768",
            ),
            valid_range=None,
            digitizer_name="CH_BLINE_NSMEAN",
        ),
        "dc_offset": CaenDT5781ParameterDefinition(
            name="DC Offset (%)",
            description="Allows the User to adjust the baseline position of the input signal on the ADC scale. The value is expressed in percentage of the input dynamic range.\nMoving the DC Offset corresponds to moving the baseline level of the input signal upward or downward in the dynamic scale to cover the full width of the pulse itself, thus avoiding saturation.\nFrom 0 to 100\nIncrements of 0.1",
            widget_type="entry",
            choices=None,
            valid_range=(0, 100),
            digitizer_name="CH_DCOFFSET",
        ),
        "coarse_gain": CaenDT5781ParameterDefinition(
            name="Coarse gain",
            description="Allows to select the input dynamic range of each channel\nGain x1, x3, x10, x33 (corresponding to 10Vpp-3Vpp-1Vpp-0.3Vpp ranges)",
            widget_type="combobox",
            choices=(
                "10",
                "3.0",
                "1.0",
                "0.3",
            ),
            valid_range=None,
            digitizer_name="CH_CGAIN",
        ),
        # Discriminator
        "threshold": CaenDT5781ParameterDefinition(
            name="Threshold (lsb)",
            description="Channel discriminator threshold\nThe units are in lsb (least significant bit)\n1 LSB = (Input dynamic range in Vpp)/2^(Nbit) [Volt]\nFrom 0 to 16383\nIncrements of 10",
            widget_type="entry",
            choices=None,
            valid_range=(0, 16383),
            digitizer_name="CH_THRESHOLD",
        ),
        "trig_holdoff": CaenDT5781ParameterDefinition(
            name="Trigger holdoff (ns)",
            description="Set the Trigger Holdoff width\nDuring the Trigger Holdoff Time other trigger signals are not accepted by the digitizer\nFrom 10 to 655350\nIncrements of 10",
            widget_type="entry",
            choices=None,
            valid_range=(10, 655350),
            digitizer_name="CH_TRG_HOLDOFF",
        ),
        "fast_smoothing": CaenDT5781ParameterDefinition(
            name="Fast discriminator smoothing",
            description="Defines the number of samples of a moving average filter used for the RC-CR2 signal formation\nThe RC-CR2 input signal second derivative smoothing value",
            widget_type="combobox",
            choices=(
                "RCCR2_SMTH_1",
                "RCCR2_SMTH_2",
                "RCCR2_SMTH_4",
                "RCCR2_SMTH_8",
                "RCCR2_SMTH_16",
                "RCCR2_SMTH_32",
            ),
            valid_range=None,
            digitizer_name="CH_RCCR2_SMOOTH",
        ),
        "rise_time": CaenDT5781ParameterDefinition(
            name="Input rise time (ns)",
            description="Value set to optimize the shape of the RC-CR2 signal used to trigger the board channels\nThis parameter defines the time constant of the derivative component of the PHA fast discriminator filter\nIn case of RC-CR2 this value must be equal (or 50% more) to the input rising edge, in such a way the RC-CR2 peak value corresponds to the height of the input signal.\nFrom 10 to 40950\nIncrements of 10",
            widget_type="entry",
            choices=None,
            valid_range=(10, 40950),
            digitizer_name="CH_RCCR2_RISE",
        ),
        # Trapezoid
        "trap_rise_time": CaenDT5781ParameterDefinition(
            name="Trap. rise time (ns)",
            description="Set the Trapezoid Rise Time\nFrom 10 to 40950\nIncrements of 10",
            widget_type="entry",
            choices=None,
            valid_range=(10, 40950),
            digitizer_name="CH_TRAP_TRISE",
        ),
        "trap_flat_top": CaenDT5781ParameterDefinition(
            name="Trap. flat top (ns)",
            description="Set the Trapezoid Flat Top width.\nFrom 10 to 40950\nIncrements of 10",
            widget_type="entry",
            choices=None,
            valid_range=(10, 40950),
            digitizer_name="CH_TRAP_TFLAT",
        ),
        "trap_pole_zero": CaenDT5781ParameterDefinition(
            name="Trap. pole zero (ns)",
            description="Set the Trapezoid Pole-Zero Cancellation. Must be set equal to the decay time of the preamplifier.\nFrom 10 to 655350\nIncrements of 10",
            widget_type="entry",
            choices=None,
            valid_range=(10, 655350),
            digitizer_name="CH_TDECAY",
        ),
        "peaking_time": CaenDT5781ParameterDefinition(
            name="Peaking time (%)",
            description="Position in percentage in the flat top region where the samples are used for the calculation of the peak height.\nThe peaking time is referred to the trigger position or to the trigger validation signal according to the trigger mode.\nIncrements of 0.1",
            widget_type="entry",
            choices=None,
            valid_range=(0, 100),
            digitizer_name="CH_TRAP_FTD",
        ),
        "samples_peak": CaenDT5781ParameterDefinition(
            name="N samples peak",
            description="Corresponds to the number of samples for the averaging window of the trapezoid height calculation.\nNote: for a correct energy calculation the Peak Mean should be contained in the flat region of the Trapezoid Flat Top.",
            widget_type="combobox",
            choices=("PEAK_NSMEAN_1", "PEAK_NSMEAN_4", "PEAK_NSMEAN_16", "PEAK_NSMEAN_64"),
            valid_range=None,
            digitizer_name="CH_PEAK_NSMEAN",
        ),
        "peak_holdoff": CaenDT5781ParameterDefinition(
            name="Peak holdoff (ns)",
            description="The Peak Hold-off starts at the end of the trapezoid flat top and defines how close must be two trapezoids to be considered piled-up.\nZero is the case where the flat top of one trapezoid starts exactly at the end of the flat top of the previous one.\nFrom 80 to 81840\nOnly multiples of 8 are allowed",
            widget_type="entry",
            choices=None,
            valid_range=(80, 81840),
            digitizer_name="CH_PEAK_HOLDOFF",
        ),
        "energy_fine_gain": CaenDT5781ParameterDefinition(
            name="Energy fine gain",
            description="Allow the User to set the fine Gain.\nFrom 1 to 10\nIncrements of 0.01",
            widget_type="entry",
            valid_range=(1, 10),
            digitizer_name="CH_FGAIN",
        ),
    }
    # Metadata
    channel_id: int
    enabled: bool = True
    # Input
    rdc_len: int = 15000
    pre_trig: int = 5000
    polarity: str = 'POLARITY_POSITIVE'
    sample_baseline: str = 'BLINE_NSMEAN_32768'
    dc_offset: float = 5.0
    coarse_gain: float = 3.0
    # Discriminator
    threshold: int = 500
    trig_holdoff: int = 480
    fast_smoothing: str = 'RCCR2_SMTH_1'
    rise_time: int = 200
    # Trapezoid
    trap_rise_time: int = 5000
    trap_flat_top: int = 1000
    trap_pole_zero: int = 1000
    peaking_time: float = 80
    samples_peak: str = 'PEAK_NSMEAN_1'
    peak_holdoff: int = 960
    energy_fine_gain: float = 1
    
    @classmethod
    def get_definitions(cls, field_name: str):
        return cls.DEFINITIONS[field_name]
    @classmethod
    def iter_digitizer_definitions(cls):
        for field_name, definition in cls.DEFINITIONS.items():
            yield field_name, definition.digitizer_name
    
    # Maps the according option to its value
    coarse_map: ClassVar[dict[float, str]] = {
        10.0  : "COARSE_GAIN_X1",   # 10  Vpp
        3.0   : "COARSE_GAIN_X3",    # 3   Vpp
        1.0   : "COARSE_GAIN_X10",    # 1   Vpp
        0.3   : "COARSE_GAIN_X33",  # 0.3 Vpp
    }
    
    def get_field_value(self, field_name: str):
        if field_name == 'coarse_gain':
            coarse_gain_float = getattr(self, field_name)
            return self.coarse_map[coarse_gain_float]
        return getattr(self, field_name)
    
    # TODO: Verify that new value is in the range/choice of the definition of the param

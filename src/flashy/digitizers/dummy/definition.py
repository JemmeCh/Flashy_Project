from flashy.models.parameters.definition import ParameterDefinition
from flashy.models.parameters.validators import validate_combo_box, validate_range_and_step

DUMMY_CHANNEL_DEFINITIONS = {
    # General
    "ch_enabled": ParameterDefinition(
        key="ch_enabled",
        name="Channel Enabled",
        description="Set if this channel is used or not",
        path="Board",
        value_type=bool,
        default=True,
        widget_type="checkbox",
        choices=None,
        valid_range=None,
        step=None,
        hardware_name="CH_ENABLED"
    ),
    "ch_id": ParameterDefinition(
        key="ch_id",
        name="Channel ID",
        description="Number given to this channel",
        path="Board",
        value_type=int,
        default=0,
        widget_type="readonly",
        choices=None,
        valid_range=None,
        step=None,
        hardware_name=None
    ),
    "rdc_len": ParameterDefinition(
        key="rdc_len",
        name="Record Lenght (ns)",
        description="Set the length of the acquisition window (in ns)\nOnly uses CH0 value.\nFrom 20 to 1310660\nIncrements of 20",
        path="Board",
        value_type=int,
        default=15000,
        widget_type="entry",
        choices=None,
        valid_range=(20, 1310660),
        step=20,
        hardware_name="RECLEN",
        validator=validate_range_and_step,
    ),
    # Input
    "coarse_gain": ParameterDefinition(
        key="coarse_gain",
        name="Coarse gain",
        description="Allows to select the input dynamic range of each channel\nGain x1, x3, x10, x33 (corresponding to 10Vpp-3Vpp-1Vpp-0.3Vpp ranges)",
        path="Input",
        value_type=float,
        default=3.0,
        widget_type="combobox",
        choices=(
            "10",
            "3.0",
            "1.0",
            "0.3",
        ),
        valid_range=None,
        hardware_name="CH_CGAIN",
        hardware_converter=lambda v: {
            10.0: "COARSE_GAIN_X1",
            3.0: "COARSE_GAIN_X3",
            1.0: "COARSE_GAIN_X10",
            0.3: "COARSE_GAIN_X33",
        }[v],
        validator=validate_combo_box,
    ),
}
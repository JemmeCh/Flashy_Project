from flashy.models.parameters.definition import ParameterDefinition
from flashy.models.parameters.parsers import parse_equation
from flashy.models.parameters.validators import validate_combo_box, validate_range_and_step

DUMMY_DEFINITIONS = {
    "digitizer_channel": ParameterDefinition(
        key="digitizer_channel",
        name="Digitizer Channel",
        description="Assign this detector to a digitizer channel to use it during analysis.",
        path="Dummy",
        value_type=int,
        default=0,
        widget_type="entry",
        valid_range=(0, 9999),
        step=1,
        validator=validate_range_and_step
    ),
    "dummy": ParameterDefinition(
        key="dummy",
        name="Dummy",
        description="This is a dummy parameter. This detector is useful for unused channels",
        path="Dummy",
        value_type=int,
        default=-1,
        widget_type="readonly"
    ),
    "Vs2C_factor": ParameterDefinition(
        key="Vs2C_factor",
        name="Facteur de conversion: [V*ns] --> [nC]",
        description="Required Volt second to Coulomb conversion factor",
        path="Dummy",
        value_type=float,
        default=2,
        widget_type="entry",
        parser=parse_equation
    ),
    "nC2cGy_factor": ParameterDefinition(
        key="nC2cGy_factor",
        name="Facteur de conversion: [nC] --> [cGy]",
        description="Permet de passer de nC à cGy\nSupporte les équations: '1 / 33.33' est valide",
        path='Dummy',
        value_type=float,
        default=2.0,
        widget_type="entry",
        choices=None,
        valid_range=None,
        parser=parse_equation
    ),
}
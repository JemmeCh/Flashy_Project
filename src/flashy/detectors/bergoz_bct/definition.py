from flashy.models.parameters.definition import ParameterDefinition
from flashy.models.parameters.parsers import parse_equation
from flashy.models.parameters.validators import validate_combo_box, validate_range_and_step

BERGOZBCT_DEFINITIONS = {
    "digitizer_channel": ParameterDefinition(
        key="digitizer_channel",
        name="Digitizer Channel",
        description="Assign this detector to a digitizer channel to use it during analysis.",
        path="Bergoz BCT",
        value_type=int,
        default=0,
        widget_type="entry",
        valid_range=(0, 9999),
        step=1,
        validator=validate_range_and_step
    ),
    "Vs2C_factor": ParameterDefinition(
        key="Vs2C_factor",
        name="Facteur de conversion: [V*ns] --> [nC]",
        description="Permet de passer de V*ns à nC\nSupporte les équations: '1 / 33.33' est valide",
        path="Bergoz BCT",
        value_type=float,
        default=1 / 33.33,
        widget_type="entry",
        parser=parse_equation
    ),
}
"""
Parameter definitions for Bergoz's BCT.

:meta hide-value:
"""
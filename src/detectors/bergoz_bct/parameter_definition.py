from src.models.parameters.parameter_definition import ParameterDefinition
from src.models.parameters.parameter_parsers import parse_equation

BERGOZBCT_DEFINITIONS = {
    "Vs2C_factor": ParameterDefinition(
        key="Vs2C_factor",
        name="Facteur de conversion: [V*ns] --> [nC]",
        description="Permet de passer de V*ns à nC\nSupporte les équations: '1 / 33.33' est valide",
        group="Bergoz BCT",
        value_type=float,
        default=1 / 33.33,
        widget_type="entry",
        parser=parse_equation
    ),
}
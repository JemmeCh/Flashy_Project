# =======================================================================
# Analysis
# =======================================================================

# =======================================================================
# Bergoz BCT
# =======================================================================

# =======================================================================
# CaenDT5781
# =======================================================================
from flashy.digitizers.caen_dt5781.definition import CAENDT5781_CHANNEL_DEFINITIONS

def iter_caen5781_parameters():
    """
    Iterate over all Caen's DT5781 digitizer channel parameters that have a corresponding
    hardware register name.
    
    Parameters whose ``hardware_name`` attribute is ``None`` are skipped.
    
    :yields: Tuples containing the parameter key and its definition.
    :rtype: tuple[str, :py:class:`~flashy.models.parameters.definition.ParameterDefinition`]
    """
    for key, definition in CAENDT5781_CHANNEL_DEFINITIONS.items():
        if definition.hardware_name is None:
            continue
        yield key, definition

def convert_to_caen5781_value(definition, value):
    """
    Convert a parameter value to the format expected by Caen's DT5781 digitizer
    hardware.
    
    If the provided parameter definition specifies a converter function, the
    converter is applied to the value. Otherwise, the value is returned
    unchanged.
    
    :param definition: Parameter definition associated with the value.
    :type definition: :py:class:`~flashy.models.parameters.definition.ParameterDefinition`
    
    :param value: Value to convert.
    :type value: Any
    
    :returns: Converted value suitable for the hardware configuration.
    :rtype: Any
    """
    if definition.hardware_converter:
        return definition.hardware_converter(value)
    return value
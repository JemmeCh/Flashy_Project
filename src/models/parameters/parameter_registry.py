# =======================================================================
# Analysis
# =======================================================================

# =======================================================================
# Bergoz BCT
# =======================================================================

# =======================================================================
# CaenDT5781
# =======================================================================
from src.digitizers.caen_dt5781.parameter_definition import CAENDT5781_CHANNEL_DEFINITIONS

def iter_caen5781_parameters():
    for key, definition in CAENDT5781_CHANNEL_DEFINITIONS.items():
        if definition.hardware_name is None:
            continue
        yield key, definition

def convert_to_caen5781_value(definition, value):
    if definition.converter:
        return definition.converter(value)
    return value
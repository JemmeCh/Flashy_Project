from src.digitizers.caen_dt5781.parameter_definition import CAENDT5781_CHANNEL_DEFINITIONS
from src.models.parameters.parameter_container import ParameterContainer


class CaenDT5781Channel(ParameterContainer):
    """Dataclass for the configuration of a DT5781 channel"""
    DEFINITIONS = CAENDT5781_CHANNEL_DEFINITIONS
    channel_id: int = -1
    enabled: bool = True
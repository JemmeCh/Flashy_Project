from flashy.digitizers.caen_dt5781.definition import CAENDT5781_CHANNEL_DEFINITIONS
from flashy.models.parameters.container import ParameterContainer


class CaenDT5781Channel(ParameterContainer):
    """
    Dataclass for the configuration of a Caen's DT5781 digitizer channel.
    
    ### Inherits:
        `ParameterContainer`
    """
    DEFINITIONS = CAENDT5781_CHANNEL_DEFINITIONS
    channel_id: int = -1
    enabled: bool = True
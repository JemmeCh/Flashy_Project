from flashy.digitizers.caen_dt5781.definition import CAENDT5781_CHANNEL_DEFINITIONS
from flashy.models.parameters.container import ParameterContainer


class CaenDT5781Channel(ParameterContainer):
    """
    Dataclass for the configuration of a Caen's DT5781 digitizer channel.
    
    :inherits: ParameterContainer
    """
    DEFINITIONS = CAENDT5781_CHANNEL_DEFINITIONS
    """
    Parameter definitions for Caen's DT5781 digitizer channels (See :py:data:`~flashy.digitizers.caen_dt5781.definition.CAENDT5781_CHANNEL_DEFINITIONS`). 
    
    :meta hide-value:
    """
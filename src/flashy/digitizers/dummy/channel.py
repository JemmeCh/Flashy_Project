from flashy.digitizers.dummy.definition import DUMMY_CHANNEL_DEFINITIONS
from flashy.models.parameters.container import ParameterContainer

class DummyDigitizerChannel(ParameterContainer):
    """
    Dataclass for the configuration of a Dummy digitizer channel.
    
    :inherits: ParameterContainer
    """
    DEFINITIONS = DUMMY_CHANNEL_DEFINITIONS
    """
    Parameter definitions for Dummy digitizer channels. 
    
    :meta hide-value:
    """
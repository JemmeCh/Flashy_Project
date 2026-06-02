from typing import Literal

from flashy.detectors.bergoz_bct.definition import BERGOZBCT_DEFINITIONS
from flashy.models.parameters.container import ParameterContainer


class BergozBCT(ParameterContainer):
    """
    Dataclass containing Bergoz's BCT configuration.
    
    :inherits: ParameterContainer
    """
    DEFINITIONS = BERGOZBCT_DEFINITIONS
    """
    Parameter definitions for Bergoz's BCT (See :py:data:`~flashy.detectors.bergoz_bct.definition.BERGOZBCT_DEFINITIONS`). 
    
    :meta hide-value:
    """
    type: Literal["bergoz_bct"] = 'bergoz_bct'
    """Fixed identifier of this detector."""
from typing import Literal

from flashy.detectors.bergoz_bct.definition import BERGOZBCT_DEFINITIONS
from flashy.models.parameters.container import ParameterContainer


class BergozBCT(ParameterContainer):
    """
    Dataclass containing Bergoz'S BCT's configuration
    
    ### Inherits:
        `ParameterContainer`
    """
    DEFINITIONS = BERGOZBCT_DEFINITIONS
    
    type: Literal["bergoz_bct"] = 'bergoz_bct'
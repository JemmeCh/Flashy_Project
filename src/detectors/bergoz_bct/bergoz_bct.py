from typing import Literal

from src.detectors.bergoz_bct.parameter_definition import BERGOZBCT_DEFINITIONS
from src.models.parameters.parameter_container import ParameterContainer


class BergozBCT(ParameterContainer):
    """Dataclass for the configuration of the Bergoz BCT"""
    DEFINITIONS = BERGOZBCT_DEFINITIONS
    
    type: Literal["bergoz_bct"] = 'bergoz_bct'
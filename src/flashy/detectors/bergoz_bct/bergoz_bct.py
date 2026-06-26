from typing import Literal

from flashy.models.parameters.container import ParameterContainer
from flashy.detectors.bergoz_bct.definition import BERGOZBCT_DEFINITIONS


class BergozBCT(ParameterContainer, tag_field="tag", tag=str.lower):
    """
    Dataclass containing Bergoz's BCT configuration.
    
    :inherits: ParameterContainer
    """
    DEFINITIONS = BERGOZBCT_DEFINITIONS
    """
    Parameter definitions for Bergoz's BCT (See :py:data:`~flashy.detectors.bergoz_bct.definition.BERGOZBCT_DEFINITIONS`). 
    
    :meta hide-value:
    """
    @property
    def display_name(self) -> str:
        return "Bergoz BCT"
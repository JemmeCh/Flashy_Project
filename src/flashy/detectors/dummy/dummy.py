from typing import Literal

from flashy.models.parameters.container import ParameterContainer
from flashy.detectors.dummy.definition import DUMMY_DEFINITIONS

class DummyDetector(ParameterContainer, tag_field="tag", tag=str.lower):
    """
    Dataclass containing Bergoz's BCT configuration.
    
    :inherits: ParameterContainer
    """
    DEFINITIONS = DUMMY_DEFINITIONS
    """
    Dummy detector class 
    
    :meta hide-value:
    """
    @property
    def display_name(self) -> str:
        return "Dummy"
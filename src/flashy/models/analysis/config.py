from flashy.models.analysis.definition import ANALYSIS_DEFINITIONS
from flashy.models.parameters.container import ParameterContainer


class AnalysisConfig(ParameterContainer):
    """
    Dataclass for the analysis' configuration.
    
    :inherits: ParameterContainer
    """
    DEFINITIONS = ANALYSIS_DEFINITIONS
    """
    Parameter definitions for analysis (See :py:data:`~flashy.models.analysis.definition.ANALYSIS_DEFINITIONS`).
    
    :meta hide-value:
    """
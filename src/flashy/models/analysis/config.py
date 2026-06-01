from flashy.models.analysis.definition import ANALYSIS_DEFINITIONS
from flashy.models.parameters.container import ParameterContainer


class AnalysisConfig(ParameterContainer):
    """
    Dataclass for the analysis' configuration.
    
    ### Inherits:
        `ParameterContainer`
    """
    DEFINITIONS = ANALYSIS_DEFINITIONS
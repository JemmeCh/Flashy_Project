from src.models.analysis.parameter_definition import ANALYSIS_DEFINITIONS
from src.models.parameters.parameter_container import ParameterContainer


class AnalysisConfig(ParameterContainer):
    """Dataclass for the configuration of an analysis"""
    DEFINITIONS = ANALYSIS_DEFINITIONS
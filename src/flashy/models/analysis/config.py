from flashy.models.analysis.definition import ANALYSIS_DEFINITIONS
from flashy.models.parameters.container import ParameterContainer
from flashy.models.tree.constructor import build_analysis_config

from typing import TYPE_CHECKING, Self
if TYPE_CHECKING:
    from flashy.models.tree.node import TreeNode

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
    @classmethod
    def from_tree(cls, root_node: "TreeNode") -> Self:
        values = build_analysis_config(root_node)
        return cls(values=values)
    
    def validate(self) -> None:
        # TODO: Implement
        pass
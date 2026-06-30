import msgspec

from flashy.models.analysis.config import AnalysisConfig
from flashy.models.acquisition_config import AcquisitionConfig

from typing import TYPE_CHECKING, Self
if TYPE_CHECKING:
    from flashy.models.tree.node import TreeNode


class ProcessingConfig(msgspec.Struct, tag_field="tag", tag=str.lower):
    """
    Parameters for processing pulses with acquisition and analysis configurations.
    
    :inherits: msgspec.Struct
    """
    acquisition: AcquisitionConfig
    """The acquisition configuration used for processing."""
    analysis: AnalysisConfig
    """The analysis configuration used for processing."""
    
    @classmethod
    def from_tree(cls, root_node: "TreeNode") -> Self:
        analysis_node = root_node.find_path("Analysis")
        if analysis_node is None: 
            raise ValueError("Couldn't find specified tree node path.")
        analysis_config = AnalysisConfig.from_tree(analysis_node)
        
        acquistion_config = AcquisitionConfig.from_tree(root_node)
        
        return cls(
            acquisition=acquistion_config,
            analysis=analysis_config
        )
    
    def validate(self) -> None:
        self.acquisition.validate()
        self.analysis.validate()
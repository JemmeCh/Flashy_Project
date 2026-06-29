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
        """
        Construct a ProcessingConfig from a configuration tree.
        
        :param root_node: Root configuration tree containing acquisition and
            analysis subtrees.
        :type root_node: TreeNode
        
        :returns: A fully constructed processing configuration.
        :rtype: Self
        
        :raises ValueError: If the analysis configuration node cannot be found.
        """
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
        """
        Validate the processing configuration.
        
        :returns: None
        :rtype: None
        
        :raises ValueError: If either acquisition or analysis configuration is invalid.
        """
        self.acquisition.validate()
        self.analysis.validate()
import msgspec

from flashy.digitizers.digitizer import Digitizer
from flashy.digitizers.map import DIGITIZER_MAP
from flashy.detectors.detector import Detector
from flashy.models.tree.constructor import (
    build_digitizer_config,
    build_detectors_config
)

from typing import TYPE_CHECKING, Self
if TYPE_CHECKING:
    from flashy.models.tree.node import TreeNode

class AcquisitionConfig(msgspec.Struct, tag_field="tag", tag=str.lower):
    """
    Parameters for an acquisition configuration.
    
    :inherits: msgspec.Struct
    """
    digitizer: Digitizer
    """Used digitizer during acquisition."""
    detectors: list[Detector]
    """List of detectors where each element represents a channel of the digitizer."""
    
    @classmethod
    def from_tree(cls, root_node: "TreeNode") -> Self:
        """
        Construct an AcquisitionConfig from a configuration tree.
        
        :param root_node: Root configuration tree containing digitizer and
            detectors subtrees.
        :type root_node: TreeNode
        
        :returns: A constructed acquisition configuration.
        :rtype: Self
        
        :raises ValueError: If required tree nodes cannot be found.
        """
        digitizer_node = root_node.find_path(
            DIGITIZER_MAP[root_node.name].display_name
        )
        if digitizer_node is None: 
            raise ValueError("Couldn't find specified tree node path.")
        detectors_node = root_node.find_path("Detectors")
        if detectors_node is None: 
            raise ValueError("Couldn't find specified tree node path.")
        
        digitizer_config = build_digitizer_config(digitizer_node)
        detectors_config = build_detectors_config(detectors_node)
        
        return cls(
            digitizer=digitizer_config,
            detectors=detectors_config
        )
    
    def validate(self) -> None:
        """
        Validate the acquisition configuration. Ensures detector assignments, 
        channel activation, and detector-channel consistency are correct before 
        acquisition begins.
        
        :returns: None
        :rtype: None
        
        :raises ValueError: If configuration constraints are violated.
        """
        self._validate_detector_assignments()
        self._validate_active_channels()
        self._validate_detector_channels()
    
    def _validate_detector_assignments(self):
        """
        Validate that each digitizer channel has at most one detector assigned.
        
        :raises ValueError: If duplicate detector channel assignments exist.
        """
        channel_ids = [det.get_value("digitizer_channel") for det in self.detectors]
        
        duplicates = {
            ch
            for ch in channel_ids
            if channel_ids.count(ch) > 1
        }
        
        if duplicates:
            raise ValueError(
                f"Multiple detectors are assigned to channels {sorted(duplicates)}."
            )
    
    def _validate_active_channels(self):
        """
        Ensure that at least one digitizer channel is enabled.
        
        :raises ValueError: If no channels are enabled.
        """
        active = [
            channel
            for channel in self.digitizer.channels
            if channel.get_value("ch_enabled")
        ]
        
        if not active:
            raise ValueError(
                "At least one digitizer channel must be enabled."
            )
    
    def _validate_detector_channels(self):
        """
        Ensure all enabled digitizer channels have an assigned detector.
        
        :raises ValueError: If enabled channels are missing detector mappings.
        """
        enabled_channels = {
            channel.get_value("ch_id")
            for channel in self.digitizer.channels
            if channel.get_value("ch_enabled")
        }
        
        detector_channels = {
            detector.get_value("digitizer_channel")
            for detector in self.detectors
        }
        
        missing_channels = enabled_channels - detector_channels
        
        if missing_channels:
            raise ValueError(
                f"The following enabled digitizer channels have no assigned detector: {sorted(missing_channels)}."
            )

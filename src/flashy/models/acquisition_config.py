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
    
    :example:
    
    .. code-block:: python
        
        AcquisitionConfig(
            digitizer=caen,
            detectors=[bergoz_bct, dummy_detector]
        )
    
    :inherits: msgspec.Struct
    """
    digitizer: Digitizer
    """Used digitizer during acquisition."""
    detectors: list[Detector]
    """List of detectors where each element represents a channel of the digitizer."""
    
    @classmethod
    def from_tree(cls, root_node: "TreeNode") -> Self:
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
        self._validate_detector_assignments()
        self._validate_active_channels()
        self._validate_detector_channels()
    
    def _validate_detector_assignments(self):
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
        enabled_channels = {
            channel.get_value("ch_id")
            for channel in self.digitizer.channels
            if channel.get_value("ch_enabled")
        }
        
        for detector in self.detectors:
            if detector.get_value("digitizer_channel") not in enabled_channels:
                raise ValueError(
                    f"{detector.display_name} is assigned to disabled channel {detector.get_value("digitizer_channel")}."
                )

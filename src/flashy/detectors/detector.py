import msgspec
from typing import Union

from flashy.detectors.bergoz_bct.bergoz_bct import BergozBCT

Detector = Union[BergozBCT]

class DetectorAssignment(msgspec.Struct):
    """
    Dataclass containing the detector and its assigned channel.
    
    :inherits: :py:class:`msgspec.Struct`
    """
    detector: Detector
    """Detector to be assigned."""
    digitizer_channel: int
    """Associated digitizer channel"""
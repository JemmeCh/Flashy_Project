import msgspec
from typing import Union

from flashy.detectors.bergoz_bct.bergoz_bct import BergozBCT
from flashy.detectors.dummy.dummy import DummyDetector

Detector = Union[BergozBCT, DummyDetector]

class DetectorAssignment(msgspec.Struct, tag=True):
    """
    Dataclass containing the detector and its assigned channel.
    
    :inherits: :py:class:`msgspec.Struct`
    """
    detector: Detector
    """Detector to be assigned."""
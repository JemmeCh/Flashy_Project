import msgspec
from typing import Union

from flashy.detectors.bergoz_bct.bergoz_bct import BergozBCT

Detector = Union[BergozBCT]

class DetectorAssignment(msgspec.Struct):
    """
    Dataclass containing the detector and its assigned channel.
    
    ### Inherits:
        `msgspec.Struct`
    """
    detector: Detector
    digitizer_channel: int
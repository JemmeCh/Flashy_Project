import msgspec
from typing import Union

from src.detectors.bergoz_bct import BergozBCT

Detector = Union[BergozBCT]

class DetectorAssignment(msgspec.Struct):
    detector: Detector
    digitizer_channel: int
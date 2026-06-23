import msgspec
from typing import Union, List

from flashy.detectors.bergoz_bct.bergoz_bct import BergozBCT
from flashy.detectors.dummy.dummy import DummyDetector

Detector = Union[DummyDetector, BergozBCT]

class DetectorsConfig(msgspec.Struct, tag_field="tag", tag=str.lower):
    detectors: List[Detector]
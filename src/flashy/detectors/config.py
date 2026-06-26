import msgspec
from typing import List

from flashy.detectors.detector import Detector

class DetectorsConfig(msgspec.Struct, tag_field="tag", tag=str.lower):
    detectors: List[Detector]
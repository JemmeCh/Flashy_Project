from typing import Union

from flashy.detectors.bergoz_bct.bergoz_bct import BergozBCT
from flashy.detectors.dummy.dummy import DummyDetector

Detector = Union[DummyDetector, BergozBCT]
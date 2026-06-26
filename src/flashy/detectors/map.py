from flashy.detectors.info import DetectorInfo
from flashy.detectors.bergoz_bct.bergoz_bct import BergozBCT
from flashy.detectors.dummy.dummy import DummyDetector

DETECTOR_MAP = {
    "bergoz_bct": DetectorInfo(
        key="bergoz_bct",
        display_name="Bergoz BCT",
        config_cls=BergozBCT,
        tag_cls="bergozbct",
    ),
    "dummy": DetectorInfo(
        key="dummy",
        display_name="Dummy",
        config_cls=DummyDetector,
        tag_cls="dummydetector",
    ),
}
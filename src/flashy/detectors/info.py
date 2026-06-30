import msgspec

from flashy.detectors.detector import Detector

class DetectorInfo(msgspec.Struct, frozen=True, tag_field="tag", tag=str.lower):
    key: str
    display_name: str
    config_cls: type[Detector]
    tag_cls: str
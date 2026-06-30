import msgspec

from flashy.digitizers.digitizer import Digitizer

class DigitizerInfo(msgspec.Struct, frozen=True, tag_field="tag", tag=str.lower):
    key: str
    display_name: str
    config_cls: type[Digitizer]
    tag_cls: str
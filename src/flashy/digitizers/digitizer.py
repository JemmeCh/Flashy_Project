import msgspec
from typing import Union, List

from flashy.digitizers.dummy.config import DummyDigitizerConfig
from flashy.digitizers.caen_dt5781.config import CaenDT5781Config

Digitizer = Union[DummyDigitizerConfig, CaenDT5781Config]

class DigitizersConfig(msgspec.Struct, tag_field="tag", tag=str.lower):
    digitizers: List[Digitizer]
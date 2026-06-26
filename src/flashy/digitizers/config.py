import msgspec
from typing import List

from flashy.digitizers.digitizer import Digitizer

class DigitizersConfig(msgspec.Struct, tag_field="tag", tag=str.lower):
    digitizers: List[Digitizer]
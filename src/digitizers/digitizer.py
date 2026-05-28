import msgspec
from typing import Union

from src.digitizers.caen_dt5781.config import CaenDT5781Config

Digitizer = Union[CaenDT5781Config]
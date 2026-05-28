import msgspec
from typing import Literal



class ParameterDefinition(msgspec.Struct):
    name: str
    description: str
    widget_type: Literal["entry", "combobox"]
    choices: tuple[str, ...] | None = None
    valid_range: tuple[float, float] | None = None

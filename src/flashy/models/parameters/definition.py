import msgspec
from typing import Literal, Any, Callable

class ParameterDefinition(msgspec.Struct, frozen=True):
    """
    Dataclass representing a parameter's metadata (immutable). 
    
    ### Inherits
        `msgspec.Struct`
    """
    key: str
    name: str
    description: str
    group: str
    
    # NOTE: Caen5781 specifically wants only str (at Caen5781Acquisition._setup_digitizer)
    value_type: type
    default: Any
    
    # TODO: Adapt to PySide6
    widget_type: Literal["entry", "combobox"]
    valid_range: tuple[float, float] | None = None
    step: int | float | None = None
    choices: tuple[Any, ...] | None = None
    
    # Setter specifics
    parser: Callable[[Any], Any] | None = None
    validator: Callable[[Any, Any], None] | None = None
    
    # Hardware specifics
    hardware_name: str | None = None
    hardware_converter: Callable[[Any], Any] | None = None
    
    # Helper methods
    def transform(self, value):
        if self.parser:
            value = self.parser(value)
        if self.validator:
            self.validator(self, value)
        value = self.value_type(value)
        return value
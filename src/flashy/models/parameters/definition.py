import msgspec
from typing import Literal, Any, Callable


class ParameterDefinition(msgspec.Struct, frozen=True):
    """
    Immutable metadata container describing a single configurable parameter.
    
    This object defines how a parameter behaves in the system, including:
    default values, validation rules, UI representation, and optional
    hardware-specific mappings.
    
    :inherits: :py:class:`msgspec.Struct`
    """
    key: str
    """Unique key identifying the parameter."""
    name: str
    """Human-readable parameter name."""
    description: str
    """Detailed description of the parameter and its behavior."""
    path: str
    """Logical grouping used for UI or organization."""
    # NOTE: Caen5781 specifically wants only str (at Caen5781Acquisition._setup_digitizer)
    value_type: type
    """Python type used to cast the parameter value after parsing/validation."""
    default: Any
    """Default value used when no override is provided."""
    widget_type: Literal["entry", "combobox", "checkbox", "readonly"]
    """
    UI widget type used to represent this parameter.
    Supported values: ``"entry"``, ``"combobox"``.
    """
    valid_range: tuple[float, float] | None = None
    """Optional valid numeric range as (min, max)."""
    step: int | float | None = None
    """Optional step size for numeric UI widgets."""
    choices: tuple[Any, ...] | None = None
    """Optional fixed set of allowed values (for combo-box style widgets)."""
    
    # =======================================================================
    # Setter specifics
    # =======================================================================
    
    parser: Callable[[Any], Any] | None = None
    """Optional preprocessing function applied before validation."""
    validator: Callable[[Any, Any], None] | None = None
    """
    Optional validation function.
    Should raise an exception if the value is invalid.
    """
    
    # =======================================================================
    # Hardware specifics
    # =======================================================================
    
    hardware_name: str | None = None
    """Name of the hardware register associated with this parameter."""
    hardware_converter: Callable[[Any], Any] | None = None
    """Optional conversion function applied when sending value to hardware."""
    
    # =======================================================================
    # Helper methods
    # =======================================================================
    
    def transform(self, value):
        """
        Transform a raw input value into a validated, typed parameter value.
        
        The transformation pipeline is:
        
        1. Apply ``parser`` if defined
        2. Validate value using ``validator`` if defined
        3. Cast value using ``value_type``
        
        :param value: Raw input value to transform.
        :type value: Any
        
        :returns: Fully processed and validated parameter value.
        :rtype: Any
        
        :raises Exception: Any exception raised by ``parser`` or ``validator``.
        """
        if self.parser:
            value = self.parser(value)
        if self.validator:
            self.validator(self, value)
        value = self.value_type(value)
        return value
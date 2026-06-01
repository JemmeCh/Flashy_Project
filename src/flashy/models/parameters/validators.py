# =======================================================================
# Validators: 
# - Used in `ParameterDefinition.transform` methods to parse user input
# - Callable[[ParameterDefinition, Any], None]
# - Raises ValueError
# - Ex: choice exists, value % 8 == 0, 0 <= value <= 16383
# =======================================================================

from functools import wraps
from decimal import Decimal
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from flashy.models.parameters.definition import ParameterDefinition

# =======================================================================
# Useful decorators
# =======================================================================

def assert_choices(func):
    @wraps(func)
    def wrapper(definition: "ParameterDefinition", *args):
        assert definition.choices, "Using combo box validation without choices"
        return func(definition, *args)
    return wrapper

def assert_valid_range(func):
    @wraps(func)
    def wrapper(definition: "ParameterDefinition", *args):
        assert definition.valid_range, "Using valid range validation without range"
        low, high = definition.valid_range
        assert low != high, "Range needs to be non-zero"
        assert low < high, f"Left value ({low}) of range needs to be the low value"
        return func(definition, *args)
    return wrapper

def assert_step(func):
    @wraps(func)
    def wrapper(definition: "ParameterDefinition", *args):
        assert definition.step, "Using step validation without step"
        return func(definition, *args)
    return wrapper

# =======================================================================
# Validators
# =======================================================================

@assert_choices
def validate_combo_box(
    definition: "ParameterDefinition", 
    value: Any
) -> None:
    """
    Validate if the input is in the choices.
    
    Args:
        definition (ParameterDefinition): The parameter's metadata.
        value (Any): Input.
    
    Raises:
        e (ValueError): The value isn't correct.
    """
    if value not in definition.choices:
        raise ValueError(f"{value} not in allowed choices: {definition.choices}")
    return

@assert_valid_range
def validate_valid_range(
    definition: "ParameterDefinition", 
    value: Any
)-> None:
    """
    Validate if the input is in the range of the parameter's range.
    
    Args:
        definition (ParameterDefinition): The parameter's metadata.
        value (Any): Input.
    
    Raises:
        e (ValueError): The value isn't correct.
    """
    low, high = definition.valid_range  #type:ignore
    if not (low <= float(value) <= high):
        raise ValueError(f"{value} outside range [{low}, {high}]")
    return

@assert_step
def validate_multiple_of_step(
    definition: "ParameterDefinition", 
    value: Any
) -> None:
    """
    Validate if the input is a multiple of the parameter's multiple.
    
    Args:
        definition (ParameterDefinition): The parameter's metadata.
        value (Any): Input.
    
    Raises:
        e (ValueError): The value isn't correct.
    """
    step = Decimal(str(definition.step))
    value_d = Decimal(str(value))
    if not (value_d % step == 0):
        raise ValueError(f"{value} must be a multiple of {definition.step} ")
    return


def validate_range_and_step(
    definition: "ParameterDefinition", 
    value: Any
) -> None:
    """
    Validate 
    1. If the input is a multiple of the parameter's multiple
    2. If the input is in the range of the parameter's range
    
    Args:
        definition (ParameterDefinition): The parameter's metadata.
        value (Any): Input.
    
    Raises:
        e (ValueError): The value isn't correct.
    """
    validate_valid_range(definition, value)
    validate_multiple_of_step(definition, value)
    return

if __name__ == '__main__':
    from flashy.models.parameters.definition import ParameterDefinition
    
    t = ParameterDefinition(
        key="area_calc_method",
        name="Méthode du calcul d'aire",
        description="'trap': Utilise la méthode des trapèzes\n'approx-HRM': Somme de toutes les points multipliée par dt (High Resolution Method)",
        group='Analysis',
        value_type=str,
        default='trap',
        widget_type="combobox",
        choices=("trap", "approx-HRM"),
        valid_range=(10, 11),
        step=0.1,
        validator=validate_range_and_step
    )
    
    
    print(t.transform("10"))
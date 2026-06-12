# =======================================================================
# Parsers: 
# - Used in `ParameterDefinition.transform` methods to parse user input
# - Callable[[Any], Any]
# - Raises SyntaxError
# - Ex: '1 / 33.33' -> float
# =======================================================================

def parse_equation(value):
    """
    Safely evaluate an equation or returns the value.
    
    :param value: The value to evaluate.
    :type value: Any
    
    :raises SyntaxError: If the equation is unsafe to parse.
    
    :returns: The evaluated result or the value.
    """
    # Source - https://stackoverflow.com/a/64471342
    # Posted by KoKlA
    # Retrieved 2026-05-29, License - CC BY-SA 4.0
    allowed_chars = "0123456789+-*(). /"
    if type(value) is str:
        for char in value:
            if char not in allowed_chars:
                raise SyntaxError("Unsafe eval")
        return eval(value)
    else: return value

if __name__ == "__main__":
    from flashy.models.parameters.definition import ParameterDefinition
    
    t = ParameterDefinition(
        key="nC2cGy_factor",
        name="Facteur de conversion: [nC] --> [cGy]",
        description="Permet de passer de nC à cGy\nRemarque: Malgré le fait que les graphiques ne sont pas affichés avec ces unités, le facteur de conversion doit respecter l'équation",
        path="Algorithms",
        value_type=float,
        default=2.0,
        widget_type="entry",
        choices=None,
        valid_range=None,
        parser=parse_equation
    )
    
    print(t.transform('1 / 33.33'))

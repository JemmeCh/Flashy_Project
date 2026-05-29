# =======================================================================
# Parsers: 
# - Callable[[Any], Any]
# - Raises SyntaxError
# =======================================================================

def parse_equation(value: str) -> float:
    # Source - https://stackoverflow.com/a/64471342
    # Posted by KoKlA
    # Retrieved 2026-05-29, License - CC BY-SA 4.0
    allowed_chars = "0123456789+-*(). /"
    for char in value:
        if char not in allowed_chars:
            raise SyntaxError("Unsafe eval")
    return eval(value)

if __name__ == "__main__":
    from src.models.parameters.parameter_definition import ParameterDefinition
    
    t = ParameterDefinition(
        key="nC2cGy_factor",
        name="Facteur de conversion: [nC] --> [cGy]",
        description="Permet de passer de nC à cGy\nRemarque: Malgré le fait que les graphiques ne sont pas affichés avec ces unités, le facteur de conversion doit respecter l'équation",
        group="Analysis",
        value_type=float,
        default=2.0,
        widget_type="entry",
        choices=None,
        valid_range=None,
        parser=parse_equation
    )
    
    print(t.transform('1 / 33.33'))

from flashy.models.parameters.definition import ParameterDefinition
from flashy.models.parameters.parsers import parse_equation
from flashy.models.parameters.validators import validate_combo_box

ANALYSIS_DEFINITIONS = {
    "use_file_analysis": ParameterDefinition(
        key="use_file_analysis",
        name="Use File Parameters",
        description="Enable to use the file's analysis parameters",
        path="User",
        value_type=bool,
        default=True,
        widget_type="checkbox"
    ),
    "area_calc_method": ParameterDefinition(
        key="area_calc_method",
        name="Méthode du calcul d'aire",
        description="'trap': Utilise la méthode des trapèzes\n'approx-HRM': Somme de toutes les points multipliée par dt (High Resolution Method)",
        path='Algorithms',
        value_type=str,
        default='trap',
        widget_type="combobox",
        choices=("trap", "approx-HRM"),
        valid_range=None,
        validator=validate_combo_box
    ),
    "level_method": ParameterDefinition(
        key='level_method',
        name="Méthode de mise à niveau",
        description="'median': Prend les 200 premiers points et utilise sa médianne pour mettre à zéro\n'dynamic-median': Calcule la dérivée du pulse pour trouver le début et la fin du pulse. Trouve la médianne des points hors-pulse et l'utilise pour mettre à zéro.\n'dynamic-mean':  Calcule la dérivée du pulse pour trouver le début et la fin du pulse. Trouve la moyenne des points hors-pulse et l'utilise pour mettre à zéro.",
        path='Algorithms',
        value_type=str,
        default='dynamic-median',
        widget_type="combobox",
        choices=("median", "dynamic-mean", "dynamic-median", "cummulative-sum"),
        valid_range=None,
        validator=validate_combo_box
    ),
    "time_scale": ParameterDefinition(
        key='time_scale',
        name="Time Scale",
        description="Scale of the time axis.",
        path='Result Panel',
        value_type=str,
        default='1e-9 (ns)',
        widget_type="combobox",
        choices=(
            "1e-9 (ns)",
            "1e-6 (μs)",
            "1e-3 (ms)",
            "1 (s)",
        ),
        valid_range=None,
        validator=validate_combo_box,
    ),
}
""" "graph1": ParameterDefinition(
        key="graph1",
        name="Graphique 1",
        description="Choix pour ce que le grahique 1 montre\nPulse: Affiche le voltage (en V) de chaque pulse selon le temps (en µs)\nAire: Affiche l'aire sous la courbe du pulse correspondant (en nC)",
        path='Graphs',
        value_type=str,
        default='Pulse',
        widget_type="combobox",
        choices=("Pulse", "Aire"),
        valid_range=None,
        validator=validate_combo_box
    ),
    "graph2": ParameterDefinition(
        key="graph2",
        name="Graphique 2",
        description="Choix pour ce que le grahique 2 montre\nPulse: Affiche le voltage (en V) de chaque pulse selon le temps (en µs)\nAire: Affiche l'aire sous la courbe du pulse correspondant (en nC)",
        path='Graphs',
        value_type=str,
        default='Pulse',
        widget_type="combobox",
        choices=("Pulse", "Aire"),
        valid_range=None,
        validator=validate_combo_box
    ), """
"""
Parameter definitions for analysis.

:meta hide-value:
"""
from flashy.models.parameters.definition import ParameterDefinition
from flashy.models.parameters.parsers import parse_equation
from flashy.models.parameters.validators import validate_combo_box

ANALYSIS_DEFINITIONS = {
    "area_calc_method": ParameterDefinition(
        key="area_calc_method",
        name="Méthode du calcul d'aire",
        description="'trap': Utilise la méthode des trapèzes\n'approx-HRM': Somme de toutes les points multipliée par dt (High Resolution Method)",
        group='Analysis',
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
        group='Analysis',
        value_type=str,
        default='dynamic_median',
        widget_type="combobox",
        choices=("median", "dynamic-mean", "dynamic-median", "cummulative-sum"),
        valid_range=None,
        validator=validate_combo_box
    ),
    "graph1": ParameterDefinition(
        key="graph1",
        name="Graphique 1",
        description="Choix pour ce que le grahique 1 montre\nPulse: Affiche le voltage (en V) de chaque pulse selon le temps (en µs)\nAire: Affiche l'aire sous la courbe du pulse correspondant (en nC)",
        group='Analysis',
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
        group="Analysis",
        value_type=str,
        default='Pulse',
        widget_type="combobox",
        choices=("Pulse", "Aire"),
        valid_range=None,
        validator=validate_combo_box
    ),
    "nC2cGy_factor": ParameterDefinition(
        key="nC2cGy_factor",
        name="Facteur de conversion: [nC] --> [cGy]",
        description="Permet de passer de nC à cGy\nSupporte les équations: '1 / 33.33' est valide",
        group="Analysis",
        value_type=float,
        default=2.0,
        widget_type="entry",
        choices=None,
        valid_range=None,
        parser=parse_equation
    ),
}
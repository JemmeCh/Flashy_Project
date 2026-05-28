import msgspec

from src.models.parameter_definition import ParameterDefinition
from src.digitizers.digitizer import Digitizer
from src.detectors.detector import DetectorAssignment

# =======================================================================
# Configurations for data 
# =======================================================================

class AcquisitionConfig(msgspec.Struct):
    """Dataclass for the parameters of an aquisition\n
        Example:\n
        ```
        AcquisitionConfig(
            digitizer=caen,
            detector_assignments=[
                DetectorAssignment(
                    detector=bergoz_1,
                    digitizer_channel=0,
                ),
                DetectorAssignment(
                    detector=bergoz_2,
                    digitizer_channel=1,
                ),
            ]
        )
        ```
    """
    digitizer: Digitizer
    detector_assignments: list[DetectorAssignment]

class AnalysisConfig(msgspec.Struct):
    """Dataclass for the configuration of an analysis"""
    # Definitions
    DEFINITIONS = {
    "area_calc_method": ParameterDefinition(
            name="Méthode du calcul d'aire",
            description="'trap': Utilise la méthode des trapèzes\n'approx-HRM': Somme de toutes les points multipliée par dt (High Resolution Method)",
            widget_type="combobox",
            choices=("trap", "approx-HRM"),
            valid_range=None,
        ),
        "level_method": ParameterDefinition(
            name="Méthode de mise à niveau",
            description="'median': Prend les 200 premiers points et utilise sa médianne pour mettre à zéro\n'dynamic-median': Calcule la dérivée du pulse pour trouver le début et la fin du pulse. Trouve la médianne des points hors-pulse et l'utilise pour mettre à zéro.\n'dynamic-mean':  Calcule la dérivée du pulse pour trouver le début et la fin du pulse. Trouve la moyenne des points hors-pulse et l'utilise pour mettre à zéro.",
            widget_type="combobox",
            choices=("median", "dynamic-mean", "dynamic-median", "cummulative-sum"),
            valid_range=None,
        ),
        "graph1": ParameterDefinition(
            name="Graphique 1",
            description="Choix pour ce que le grahique 1 montre\nPulse: Affiche le voltage (en V) de chaque pulse selon le temps (en µs)\nAire: Affiche l'aire sous la courbe du pulse correspondant (en nC)",
            widget_type="combobox",
            choices=("Pulse", "Aire"),
            valid_range=None,
        ),
        "graph2": ParameterDefinition(
            name="Graphique 2",
            description="Choix pour ce que le grahique 2 montre\nPulse: Affiche le voltage (en V) de chaque pulse selon le temps (en µs)\nAire: Affiche l'aire sous la courbe du pulse correspondant (en nC)",
            widget_type="combobox",
            choices=("Pulse", "Aire"),
            valid_range=None,
        ),
        "nC2cGy_factor": ParameterDefinition(
            name="Facteur de conversion: [nC] --> [cGy]",
            description="Permet de passer de nC à cGy\nRemarque: Malgré le fait que les graphiques ne sont pas affichés avec ces unités, le facteur de conversion doit respecter l'équation",
            widget_type="entry",
            choices=None,
            valid_range=None,
        ),
    }
    
    # Data
    area_calc_method: str = 'trap'
    level_method: str = 'dynamic_median'
    graph1: str = 'Pulse'
    graph2: str = 'Pulse'
    nC2cGy_factor: float = 2.0

class ProcessingConfig(msgspec.Struct):
    """Dataclass for processing pulses with specific aquisition and analysis parameters"""
    acquisition: AcquisitionConfig
    analysis: AnalysisConfig
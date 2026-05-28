import numpy as np
from typing import Literal

from src.models.parameter_definition import ParameterDefinition
from src.detectors.base_detector import BaseDetector

class BergozBCT(BaseDetector):
    # Definitions
    DEFINITIONS = {
        "Vs2C_factor": ParameterDefinition(
            name="Facteur de conversion: [V*s] --> [C]",
            description="Permet de passer de V*s à C\nRemarque: Malgré le fait que les graphiques ne sont pas affichés avec ces unités, le facteur de conversion doit respecter l'équation",
            widget_type="entry",
            choices=None,
            valid_range=None,
        ),
    }
    
    # Metadata
    type: Literal["bergoz_bct"] = 'bergoz_bct'
    
    # Facteur de calibration fourni par le fabricant
    convertion_factor: float = 1 / 33.33
    
    def get_vns_to_nc_factor(self) -> float:
        # [V*ns] --> [V*s]
        temp = 1e9
        # [V*s] --> [C]
        temp *= self.convertion_factor
        # [C] --> [nC] 
        temp *= 1e-9
        return temp
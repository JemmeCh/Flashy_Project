import msgspec

from src.models.analysis.config import AnalysisConfig
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

class ProcessingConfig(msgspec.Struct):
    """Dataclass for processing pulses with specific aquisition and analysis parameters"""
    acquisition: AcquisitionConfig
    analysis: AnalysisConfig
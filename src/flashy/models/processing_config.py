import msgspec

from flashy.models.analysis.config import AnalysisConfig
from flashy.digitizers.digitizer import Digitizer
from flashy.detectors.detector import DetectorAssignment

# =======================================================================
# Configurations for data 
# =======================================================================

class AcquisitionConfig(msgspec.Struct):
    """
    Parameters for an acquisition configuration.
    
    :example:
    
    .. code-block:: python
        
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
    
    :inherits: msgspec.Struct
    """
    digitizer: Digitizer
    """Used digitizer during acquisition."""
    detector_assignments: list[DetectorAssignment]
    """List of detectors where each element represents a channel of the digitizer."""

class ProcessingConfig(msgspec.Struct):
    """
    Parameters for processing pulses with acquisition and analysis configurations.
    
    :inherits: msgspec.Struct
    """
    acquisition: AcquisitionConfig
    """The acquisition configuration used for processing."""
    analysis: AnalysisConfig
    """The analysis configuration used for processing."""
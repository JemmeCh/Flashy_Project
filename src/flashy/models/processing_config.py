import msgspec

from flashy.models.analysis.config import AnalysisConfig
from flashy.digitizers.digitizer import Digitizer
from flashy.detectors.detector import Detector

# =======================================================================
# Configurations for data 
# =======================================================================

class AcquisitionConfig(msgspec.Struct, tag_field="tag", tag=str.lower):
    """
    Parameters for an acquisition configuration.
    
    :example:
    
    .. code-block:: python
        
        AcquisitionConfig(
            digitizer=caen,
            detectors=[bergoz_bct, detector=dummy_detector]
        )
    
    :inherits: msgspec.Struct
    """
    digitizer: Digitizer
    """Used digitizer during acquisition."""
    detectors: list[Detector]
    """List of detectors where each element represents a channel of the digitizer."""

class ProcessingConfig(msgspec.Struct, tag_field="tag", tag=str.lower):
    """
    Parameters for processing pulses with acquisition and analysis configurations.
    
    :inherits: msgspec.Struct
    """
    acquisition: AcquisitionConfig
    """The acquisition configuration used for processing."""
    analysis: AnalysisConfig
    """The analysis configuration used for processing."""
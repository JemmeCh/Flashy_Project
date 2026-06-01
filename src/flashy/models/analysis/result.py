import numpy as np
import msgspec

from typing import List

from flashy.models.processing_config import ProcessingConfig
from flashy.models.batch_pulses import BatchPulses


class AnalysisResult(msgspec.Struct):
    """
    Container for results of an analysis for each channel.
    
    ### Inherits
        `msgspec.Struct`
    """
    pulse_batches: List[BatchPulses]
    config: ProcessingConfig
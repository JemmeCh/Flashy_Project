import numpy as np
import msgspec

from typing import List

from flashy.models.processing_config import ProcessingConfig
from flashy.models.batch_pulses import BatchPulses


class AnalysisResult(msgspec.Struct):
    """
    Container for results of an analysis for each channel.
    
    :inherits: :py:class:`msgspec.Struct`
    """
    pulse_batches: List[BatchPulses]
    """Resulting batch of pulses. Each element represents a channel's result."""
    config: ProcessingConfig
    """The processing configuration used for the analysis."""
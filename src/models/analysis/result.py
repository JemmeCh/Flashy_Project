import numpy as np
import msgspec

from typing import List

from src.models.processing_config import ProcessingConfig
from src.models.batch_pulses import BatchPulses


class AnalysisResult(msgspec.Struct):
    pulse_batches: List[BatchPulses]
    config: ProcessingConfig
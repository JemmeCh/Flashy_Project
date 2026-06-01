from PySide6.QtCore import QThread, Signal
import queue
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flashy.models.processing_config import ProcessingConfig

from flashy.services.analysis_service import AnalysisService
from flashy.models.analysis.result import AnalysisResult

class AnalysisWorker(QThread):
    """
    Wrapper class for the analysis service to be used in a seperate thread.
    
    ### Inherits:
        `PySide6.QtCore.QThread`
    """
    analysis_complete = Signal(AnalysisResult)
    
    def __init__(self, analysis_queue: queue.Queue, config: "ProcessingConfig") -> None:
        super().__init__()
        self.queue: queue.Queue[list] = analysis_queue
        self.config: "ProcessingConfig" = config
        self._is_running = True
        
        self.analyser = AnalysisService()
    
    def run(self):
        """
        Run method: analyses a list of `BatchPulses` in the queue.
        """
        while self._is_running:
            try:
                batch = self.queue.get(timeout=0.1)
                result = self.analyser.analyse_real_time(batch, self.config)
                self.analysis_complete.emit(result)
            except queue.Empty:
                continue
    
    def stop(self):
        """
        Stops the `run` method as requested by main thread.
        """
        self._is_running = False
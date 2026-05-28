from PySide6.QtCore import QObject, QThread, Signal
import queue
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.models.data_config import ProcessingConfig

from src.services.analysis_service import AnalysisService
from src.models.analysis_result import AnalysisResult

class AnalysisWorker(QThread):
    analysis_complete = Signal(AnalysisResult)
    
    def __init__(self, analysis_queue: queue.Queue, config: "ProcessingConfig") -> None:
        super().__init__()
        self.queue: queue.Queue[list] = analysis_queue
        self.config: "ProcessingConfig" = config
        self._is_running = True
        
        self.analyser = AnalysisService()
    
    def run(self):
        while self._is_running:
            try:
                batch = self.queue.get(timeout=0.1)
                result = self.analyser.analyse_real_time(batch, self.config)
                self.analysis_complete.emit(result)
            except queue.Empty:
                continue
    
    def stop(self):
        """Request stop from main thread"""
        self._is_running = False
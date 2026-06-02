from PySide6.QtCore import QThread, Signal
import queue
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from flashy.models.processing_config import ProcessingConfig

from flashy.services.analysis_service import AnalysisService
from flashy.models.analysis.result import AnalysisResult


class AnalysisWorker(QThread):
    """
    Worker thread that executes real-time analysis in a background loop.

    This class wraps :class:`AnalysisService` and continuously consumes data
    from a queue, processing it asynchronously and emitting results back to
    the main thread.

    :inherits: :py:class:`PySide6.QtCore.QThread`
    """
    analysis_complete = Signal(AnalysisResult)
    """Emitted when a batch has been successfully analysed."""
    
    def __init__(self, analysis_queue: queue.Queue, config: "ProcessingConfig") -> None:
        """
        Initialize the analysis worker thread.
        
        :param analysis_queue: Queue containing incoming data batches.
        :type analysis_queue: queue.Queue
        
        :param config: Processing configuration used for analysis.
        :type config: ProcessingConfig
        """
        super().__init__()
        self.queue: queue.Queue[list] = analysis_queue
        """Queue of incoming data batches to be processed."""
        self.config: "ProcessingConfig" = config
        """Processing configuration used for analysis."""
        self._is_running = True
        """Internal flag controlling thread execution."""
        
        self.analyser: "AnalysisService" = AnalysisService()
        """Service responsible for performing analysis computations."""
    
    def run(self):
        """
        Main thread loop.
        
        Continuously retrieves batches from the queue and processes them using
        :class:`AnalysisService`. Results are emitted via ``analysis_complete``.
        
        The loop blocks briefly on the queue (timeout = 0.1s) to allow
        responsive shutdown.
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
        Request the worker thread to stop execution.
        
        The thread will exit after the next queue timeout.
        """
        self._is_running = False
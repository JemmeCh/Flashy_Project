from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from flashy.models.analysis.result import AnalysisResult
from flashy.services.logger.logger_service import get_logger

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flashy.app_context import AppContext


class PresenterAnalyser(qtc.QObject):
    results_ready = qtc.Signal(AnalysisResult)
    
    def __init__(
        self,
        app_context: "AppContext"
    ):
        super().__init__()
        self._serv_analysis = app_context.serv_analysis
        self._logger = get_logger()
    
    @qtc.Slot(str)
    def analyse_file(self, filename: str):
        # TODO: Check if user want to use custom analyser parameters
        try:
            analysis_results = self._serv_analysis.analyse_file(filename)
            self.results_ready.emit(analysis_results)
            self._logger.info(f"Analysis of {filename} finished!")
        except Exception as e:
            self._logger.exception("File couldn't be analysed correctly")
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
    send_change_analyser_root = qtc.Signal(str)
    
    def __init__(
        self,
        app_context: "AppContext"
    ):
        super().__init__()
        self._serv_analysis = app_context.serv_analysis
        self._logger = get_logger()
        self._analysis = app_context.analysis_config
    
    @qtc.Slot(str)
    def analyse_file(self, filename: str):
        analysis_config = None
        if self._analysis.get_value("use_file_analysis"):
            self._logger.info("Using file analysis config.")
        else:
            analysis_config = self._analysis
            self._logger.info("Using custom analysis config.")
        try:
            analysis_results = self._serv_analysis.analyse_file(filename, analysis_config)
            self.results_ready.emit(analysis_results)
            self._logger.info(f"Analysis of {filename} finished!")
        except Exception as e:
            self._logger.exception("File couldn't be analysed correctly.")
    
    @qtc.Slot(str)
    def change_analyser_root(self, root: str):
        self.send_change_analyser_root.emit(root)
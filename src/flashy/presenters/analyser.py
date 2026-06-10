from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flashy.gui.widgets.analyser_controls_widget import AnalyserControlsWidget
    from flashy.gui.widgets.result_panel_widget import ResultPanelWidget

from flashy.services.analysis_service import AnalysisService


class PresenterAnalyser(qtw.QWidget):
    def __init__(
        self,
        controls: "AnalyserControlsWidget",
        result_panel: "ResultPanelWidget",
        analysis_service: "AnalysisService | None" = None,
    ):
        super().__init__()
        self._controls = controls
        self._result_panel = result_panel
        
        if analysis_service: self._analyser = analysis_service
        else: self._analyser = AnalysisService()
        
        self._controls.pressed_analyse_file.connect(self._on_analyse_file_pressed)
    
    @qtc.Slot(str)
    def _on_analyse_file_pressed(self, filename: str):
        # TODO: Check if user want to use custom analyser parameters
        try:
            analysis_results = self._analyser.analyse_file(filename)
            self._result_panel.change_results(analysis_results)
        except Exception as e:
            # TODO: emit the error to a error handler
            print(str(e))
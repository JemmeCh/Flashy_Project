from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from flashy.services.acquisition.acquisition_service import AcquisitionService
from flashy.services.acquisition.state import AcquisitionState
from flashy.services.logger.logger_service import get_logger
from flashy.models.analysis.result import AnalysisResult
from flashy.models.batch_pulses import BatchPulses

from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from flashy.app_context import AppContext


class PresenterDT5781(qtc.QObject):
    send_set_enable_other_tabs = qtc.Signal(bool)
    send_set_enable_controls = qtc.Signal(bool)
    send_set_enable_results = qtc.Signal(bool)
    state_changed = qtc.Signal(AcquisitionState)
    send_new_results = qtc.Signal(AnalysisResult)
    
    def __init__(
        self,
        app_context: "AppContext"
    ):
        super().__init__()
        self._logger = get_logger()
        self._app_context = app_context
        
        self._acquisition = None
    
    @qtc.Slot()
    def start_acquisition(self):
        self._set_enables(False)
        if not self._acquisition:
            self._acquisition = AcquisitionService(self._app_context.processing_config)
        self._acquisition.begin_acquisition(
            signal_state_changed=self.state_changed,
            digitizer="caen_dt5781"
        )
    
    @qtc.Slot()
    def stop_acquisition(self):
        self._set_enables(True)
        if self._acquisition:
            self._acquisition.stop_acquisition()
            self._acquisition.shutdown()
    
    @qtc.Slot('List[BatchPulses]')
    def results_changed(self, list_results: List[BatchPulses]):
        package = AnalysisResult(
            pulse_batches=list_results,
            config=self._app_context.processing_config
        )
        self.send_new_results.emit(package)
    
    # =======================================================================
    # Helper methods 
    # =======================================================================
    
    def _set_enables(self, enable: bool) -> None:
        self.send_set_enable_other_tabs.emit(enable)
        self.send_set_enable_controls.emit(enable)
        self.send_set_enable_results.emit(enable)
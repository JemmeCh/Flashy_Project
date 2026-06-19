from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from time import sleep

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
    increment_changed = qtc.Signal()
    
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
        self._logger.debug("Starting Acquisition Service")
        self._set_enables(False)
        self._acquisition = AcquisitionService(self._app_context.processing_config)
        self._acquisition.results_changed.connect(
            self.results_changed
        )
        self._acquisition.begin_acquisition(
            signal_state_changed=self.state_changed,
            digitizer="caen_dt5781"
        )
        self._acquisition.acquisition_finished.connect(
            self.acquisition_finished
        )
    
    @qtc.Slot()
    def stop_acquisition(self):
        self._logger.debug("Stopping Acquisition Service")
        self._set_enables(True)
        if self._acquisition:
            self._acquisition.stop_acquisition()
    
    @qtc.Slot('List[BatchPulses]')
    def results_changed(self, list_results: List[BatchPulses]):
        for batch in list_results:
            if not batch.has_pulses:
                self._logger.info('No pulse detected.')
                return
        package = AnalysisResult(
            pulse_batches=list_results,
            config=self._app_context.processing_config
        )
        self.send_new_results.emit(package)
    
    @qtc.Slot('List[BatchPulses]')
    def acquisition_finished(self, list_results: List[BatchPulses]):
        self._app_context.serv_exporter.write_post_acquisition_to_tdms(
            list_results,
            self._app_context.user_config.get_value('path_of_shoot')+".tdms",
            self._app_context.processing_config
        )
        self._app_context.user_config.set_value(
            'increment', self._app_context.user_config.get_value('increment')+1
        )
        self.increment_changed.emit()
    
    # =======================================================================
    # Helper methods 
    # =======================================================================
    
    def _set_enables(self, enable: bool) -> None:
        self.send_set_enable_other_tabs.emit(enable)
        self.send_set_enable_controls.emit(enable)
        self.send_set_enable_results.emit(enable)
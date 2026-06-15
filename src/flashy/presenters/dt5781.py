from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from flashy.services.acquisition_service import AcquisitionService
from flashy.services.logger.logger_service import get_logger

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flashy.app_context import AppContext


class PresenterDT5781(qtc.QObject):
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
        if not self._acquisition:
            self._acquisition = AcquisitionService(self._app_context.processing_config)
        self._acquisition.begin_acquisition(digitizer="caen_dt5781")
    
    @qtc.Slot()
    def stop_acquisition(self):
        if self._acquisition:
            self._acquisition.stop_acquisition()
            self._acquisition.shutdown()
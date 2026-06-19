from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from flashy.gui.ui.ui_dt5781_controls import Ui_DT5781ControlsWidget
from flashy.gui.treeview.parameter_treeview import ParameterTreeView
from flashy.gui.widgets.acquisition_timer import AcquisitionTimer

from flashy.services.acquisition.state import AcquisitionState
from flashy.services.logger.logger_service import get_logger

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flashy.app_context import AppContext

class DT5781ControlsWidget(qtw.QWidget, Ui_DT5781ControlsWidget):
    pressed_change_project = qtc.Signal()
    pressed_change_shoot = qtc.Signal()
    start_acquisition = qtc.Signal()
    stop_acquisition = qtc.Signal()
    
    def __init__(
        self,
        app_context: "AppContext",
        parent=None
    ):
        super().__init__(parent)
        self.setupUi(self)
        self._acq_running = False
        self._user_config = app_context.user_config
        self._logger = get_logger()
        
        # Replace placeholder with custom widgets
        self.tv_parameters = ParameterTreeView(app_context.processing_root_tree)
        self.acq_timer = AcquisitionTimer(self)
        self.layout_Parameters.replaceWidget(self.ParameterTreeViewPlaceholder, self.tv_parameters)
        self.layout_digitizer.replaceWidget(self.LCDTimerPlaceholder, self.acq_timer)
        self.ParameterTreeViewPlaceholder.setParent(None)
        self.LCDTimerPlaceholder.setParent(None)
        
        # Setup acquisition tab
        self.le_status.selectionChanged.connect(lambda: self.le_status.setSelection(0, 0))
        self.le_next_shoot.selectionChanged.connect(lambda: self.le_next_shoot.setSelection(0, 0))
        
        # TODO: Change this to proper model
        self.le_project.setText(self._user_config.get_value('project_path'))
        self.le_shoot.setText(self._user_config.get_value('name_of_shoot'))
        self.le_next_shoot.setText(self._user_config.get_value('increment_name'))
        self.le_status.setText("Disconnected")
        
        # Push button connections
        self.pb_acquisition.clicked.connect(self.toggle_acquisition)
        self.pb_project.clicked.connect(self.change_project)
        self.pb_shoot.clicked.connect(self.change_shoot)
    
    @qtc.Slot()
    def toggle_acquisition(self):
        self.acq_timer.toggle_timer()
        if not self._acq_running:
            self.pb_acquisition.setText('Stop Acquisition')
            self._acq_running = True
            self.start_acquisition.emit()
        else:
            self.pb_acquisition.setText('Begin Acquisition')
            self._acq_running = False
            self.stop_acquisition.emit()
    
    @qtc.Slot()
    def change_project(self):
        dialog = qtw.QFileDialog()
        dialog.setFileMode(qtw.QFileDialog.FileMode.Directory)
        if dialog.exec():
            try:
                new_path = dialog.selectedFiles()[0]
                self._user_config.set_value('project_path', new_path)
                self.le_project.setText(new_path)
                self._logger.info(f"Project path set to: {new_path}")
            except Exception as e:
                self._logger.exception("Failed to change project directory")
    
    @qtc.Slot()
    def change_shoot(self):
        new_name = self.le_shoot.text()
        try:
            self._user_config.set_value('name_of_shoot', new_name)
            self._logger.info(f"Shoot name set to: {new_name}")
        except Exception:
            self._logger.exception("Failed to change shoot name")
        self.increment_changed()
    
    @qtc.Slot(bool)
    def set_enabled_controls(self, enable: bool):
        # Tab navigation
        index = self.tab_holder.currentIndex()
        for i in range(self.tab_holder.count()):
            if i != index: self.tab_holder.setTabEnabled(i, enable)
        # User settings
        self.gb_project.setEnabled(enable)
    
    @qtc.Slot(AcquisitionState)
    def state_changed(self, state: AcquisitionState):
        self.le_status.setText(state.name)
        
        if state == AcquisitionState.ERROR:
            self.toggle_acquisition()
    
    @qtc.Slot()
    def increment_changed(self):
        inc_name = self._user_config.get_value('increment_name')
        self.le_next_shoot.setText(inc_name)
        change_name = self._user_config.get_value('name_of_shoot')
        self.le_shoot.setText(change_name)


if __name__ == '__main__':
    import sys
    
    from flashy.gui.theme import FLASHy_THEME
    from flashy.app_context import AppContext
    qtw.QApplication.setStyle("Fusion")
    
    app_context = AppContext()
    
    app = qtw.QApplication(sys.argv)
    app.setPalette(FLASHy_THEME)
    
    w1 = DT5781ControlsWidget(app_context)
    w1.show()
    
    w1.start_acquisition.connect(lambda: print('Acquisition started!'))
    w1.stop_acquisition.connect(lambda: print('Acquisition stopped!'))
    
    sys.exit(app.exec())
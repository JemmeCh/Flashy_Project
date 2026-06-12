from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from flashy.gui.ui.ui_dt5781_controls import Ui_DT5781ControlsWidget
from flashy.gui.treeview.parameter_treeview import ParameterTreeView
from flashy.gui.widgets.acquisition_timer import AcquisitionTimer

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flashy.models.tree.node import TreeNode
    from flashy.models.user_config import UserConfig

class DT5781ControlsWidget(qtw.QWidget, Ui_DT5781ControlsWidget):
    start_acquisition = qtc.Signal()
    stop_acquisition = qtc.Signal()
    def __init__(
        self,
        root_node: "TreeNode", 
        user_config: "UserConfig",
        parent=None
    ):
        super().__init__(parent)
        self.setupUi(self)
        self._root_node = root_node
        self._user_config = user_config
        self._acq_running = False
        
        # Replace placeholder with custom widgets
        self.tv_parameters = ParameterTreeView(self._root_node)
        self.acq_timer = AcquisitionTimer(self)
        self.layout_Parameters.replaceWidget(self.ParameterTreeViewPlaceholder, self.tv_parameters)
        self.layout_digitizer.replaceWidget(self.LCDTimerPlaceholder, self.acq_timer)
        self.ParameterTreeViewPlaceholder.setParent(None)
        self.LCDTimerPlaceholder.setParent(None)
        
        # Setup acquisition tab
        self.le_status.selectionChanged.connect(lambda: self.le_status.setSelection(0, 0))
        self.le_next_shoot.selectionChanged.connect(lambda: self.le_next_shoot.setSelection(0, 0))
        self.le_project.setText(self._user_config.project_path)
        self.le_shoot.setText(self._user_config.name_of_shoot)
        self.le_next_shoot.setText(self._user_config.increment_name)
        self.le_status.setText("Disconnected")
        
        # Connections
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
        pass
    
    @qtc.Slot()
    def change_shoot(self):
        pass


if __name__ == '__main__':
    import sys
    from flashy.models.tree.constructor import _make_test_config, construct_tree
    from flashy.models.user_config import UserConfig
    from flashy.gui.theme import FLASHy_THEME
    qtw.QApplication.setStyle("Fusion")
    
    root_node = construct_tree(_make_test_config())
    user_config = UserConfig()
    
    app = qtw.QApplication(sys.argv)
    app.setPalette(FLASHy_THEME)
    
    #wid = qtw.QWidget()
    #layout = qtw.QHBoxLayout()  # Horizontal = side-by-side
    w1 = DT5781ControlsWidget(root_node, user_config)
    #w2 = AnalyserControlsWidget(root_node)
    
    #layout.addWidget(w1)
    #layout.addWidget(w2)
    
    #wid.setLayout(layout)
    #wid.show()
    w1.show()
    
    w1.start_acquisition.connect(lambda: print('Acquisition started!'))
    w1.stop_acquisition.connect(lambda: print('Acquisition stopped!'))
    
    sys.exit(app.exec())
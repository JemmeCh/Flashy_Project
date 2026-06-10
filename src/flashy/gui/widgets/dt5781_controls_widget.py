from PySide6 import QtWidgets as qtw

from flashy.gui.ui.ui_dt5781_controls import Ui_DT5781ControlsWidget

class DT5781ControlsWidget(qtw.QWidget, Ui_DT5781ControlsWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setupUi(self)
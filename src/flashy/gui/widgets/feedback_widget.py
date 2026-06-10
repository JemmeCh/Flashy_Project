from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from flashy.gui.ui.ui_feedback_widget import Ui_FeedbackWidget
from flashy.services.logger.qt_handler import emitter

class FeedbackWidget(qtw.QWidget, Ui_FeedbackWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Connections
        emitter.message_logged.connect(self.append_message)
    
    @qtc.Slot(str)
    def append_message(self, msg: str):
        self.plainTextEdit.appendPlainText(msg)
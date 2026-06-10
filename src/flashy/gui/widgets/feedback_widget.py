from PySide6 import QtWidgets as qtw

from flashy.gui.ui.ui_feedback_widget import Ui_FeedbackWidget

class FeedbackWidget(qtw.QWidget, Ui_FeedbackWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setupUi(self)
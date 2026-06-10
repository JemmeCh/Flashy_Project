import sys

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from flashy.gui.theme import FLASHy_THEME

from flashy.gui.ui.ui_flashy_window import Ui_MainWindow
from flashy.gui.tabs.analyser_tab import TabAnalyser
from flashy.gui.tabs.dt5781_tab import TabDT5781
from flashy.gui.widgets.feedback_widget import FeedbackWidget

from flashy.services.logger.logger_service import setup_logging


class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        
        # Replace placeholder with custom widgets
        self.w_tab_analyser = TabAnalyser()
        self.w_tab_dt5781 = TabDT5781()
        self.w_feedback = FeedbackWidget()
        
        self.layout_TabAnalyser.replaceWidget(self.TabAnalyserPlaceholder, self.w_tab_analyser)
        self.layout_TabDT5781.replaceWidget(self.TabDT5781Placeholder, self.w_tab_dt5781)
        self.layout_window.replaceWidget(self.FeedbackPlaceholder, self.w_feedback)
        
        self.TabAnalyserPlaceholder.setParent(None)
        self.TabDT5781Placeholder.setParent(None)
        self.FeedbackPlaceholder.setParent(None)
        
        # Tag
        tag = qtw.QLabel('2024-2026 | [NOM DU LAB] | FLASHy 1.7.0  ')
        font = qtg.QFont()
        font.setItalic(True)
        tag.setFont(font)
        self.status_bar.addPermanentWidget(tag)


if __name__ == '__main__':
    qtw.QApplication.setStyle("Fusion")
    setup_logging()
    
    app = qtw.QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    app.setPalette(FLASHy_THEME)
    sys.exit(app.exec())
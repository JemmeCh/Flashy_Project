import sys

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from flashy.gui.ui.ui_flashy_window import Ui_MainWindow
from flashy.gui.tabs.analyser_tab import TabAnalyser
from flashy.gui.tabs.dt5781_tab import TabDT5781
from flashy.gui.widgets.feedback_widget import FeedbackWidget

import flashy.gui.ui.ressources_rc

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flashy.app_context import AppContext


class MainWindow(qtw.QMainWindow, Ui_MainWindow):
    def __init__(
        self,
        app_context: "AppContext"
    ):
        super().__init__()
        self.setupUi(self)
        
        self._app = app_context
        
        # Replace placeholder with custom widgets
        self.w_tab_analyser = TabAnalyser(self._app, parent=self)
        self.w_tab_dt5781 = TabDT5781(self._app)
        self.w_feedback = FeedbackWidget()
        
        self.layout_TabAnalyser.replaceWidget(self.TabAnalyserPlaceholder, self.w_tab_analyser)
        self.layout_TabDT5781.replaceWidget(self.TabDT5781Placeholder, self.w_tab_dt5781)
        self.layout_window.replaceWidget(self.FeedbackPlaceholder, self.w_feedback)
        
        self.TabAnalyserPlaceholder.setParent(None)
        self.TabDT5781Placeholder.setParent(None)
        self.FeedbackPlaceholder.setParent(None)
        
        # Conenctions for dis/enabling tab navigation
        self.w_tab_dt5781.pres_dt5781.send_set_enable_other_tabs.connect(
            self.set_enabled_other_tabs
        )
        
        # Tag and icon
        icon = qtg.QIcon()
        icon.addFile(u":/Logo/logo.png", qtc.QSize(), qtg.QIcon.Mode.Normal, qtg.QIcon.State.Off)
        self.setWindowIcon(icon)
        tag = qtw.QLabel("2024-2026 | Laboratoire d'Arthur Lalonde | FLASHy 1.8.0  ")
        font = qtg.QFont()
        font.setItalic(True)
        tag.setFont(font)
        self.status_bar.addPermanentWidget(tag)
    
    @qtc.Slot(bool)
    def set_enabled_other_tabs(self, enable: bool):
        index = self.tab_holder.currentIndex()
        for i in range(self.tab_holder.count()):
            if i != index: self.tab_holder.setTabEnabled(i, enable)
    
    @qtc.Slot()
    def on_quit(self):
        self._app.serv_exporter.save_config_to_json(
            self._app.user_config, 
            self._app.analysis_config,
            self._app.digitizers_config,
            self._app.detectors_config,
        )


def main():
    from flashy.app_context import AppContext
    from flashy.gui.theme import FLASHy_THEME
    qtw.QApplication.setStyle("Fusion")
    app_context = AppContext()
    
    app = qtw.QApplication(sys.argv)
    app.setPalette(FLASHy_THEME)
    
    window = MainWindow(app_context)
    window.show()
    
    app.aboutToQuit.connect(window.on_quit)
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
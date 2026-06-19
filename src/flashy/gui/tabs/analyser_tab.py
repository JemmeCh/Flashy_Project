from PySide6 import QtWidgets as qtw

from flashy.gui.ui.ui_analyser_tab import Ui_TabAnalyser
from flashy.gui.widgets.analyser_controls_widget import AnalyserControlsWidget
from flashy.gui.widgets.result_panel_widget import ResultPanelWidget

from flashy.presenters.analyser import PresenterAnalyser

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flashy.app_context import AppContext

class TabAnalyser(qtw.QWidget, Ui_TabAnalyser):
    def __init__(
        self, 
        app_context: "AppContext",
        parent = None,
    ):
        super().__init__(parent)
        self.setupUi(self)
        
        # Replace placeholder widgets with custom widgets
        self.w_analyser_controls = AnalyserControlsWidget(app_context)
        self.w_result_panel = ResultPanelWidget()
        
        self.layout_LeftPanel.replaceWidget(self.ControlsWidgetPlaceholder, self.w_analyser_controls)
        self.layout_ResultPanel.replaceWidget(self.ResultPanelPlaceholder, self.w_result_panel)
        
        self.ControlsWidgetPlaceholder.setParent(None)
        self.ResultPanelPlaceholder.setParent(None)
        
        # Initiate presenter + connections
        self.pres_analyser = PresenterAnalyser(app_context)
        self.pres_analyser.results_ready.connect(
            self.w_result_panel.change_results
        )
        self.w_analyser_controls.pressed_analyse_file.connect(
            self.pres_analyser.analyse_file
        )

if __name__ == '__main__':
    import sys
    
    from flashy.gui.theme import FLASHy_THEME
    from flashy.app_context import AppContext
    qtw.QApplication.setStyle("Fusion")
    
    app_context = AppContext()
    
    app = qtw.QApplication(sys.argv)
    app.setPalette(FLASHy_THEME)
    
    tab = TabAnalyser(app_context)
    tab.show()
    
    sys.exit(app.exec())
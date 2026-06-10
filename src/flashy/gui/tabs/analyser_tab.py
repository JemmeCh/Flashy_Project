from PySide6 import QtWidgets as qtw

from flashy.gui.ui.ui_analyser_tab import Ui_TabAnalyser
from flashy.gui.widgets.analyser_controls_widget import AnalyserControlsWidget
from flashy.gui.widgets.result_panel_widget import ResultPanelWidget

from flashy.services.analysis_service import AnalysisService

from flashy.presenters.analyser import PresenterAnalyser

class TabAnalyser(qtw.QWidget, Ui_TabAnalyser):
    def __init__(
        self, 
        parent = None,
    ):
        super().__init__(parent)
        self.setupUi(self)
        
        # Replace placeholder widgets with custom widgets
        self.w_analyser_controls = AnalyserControlsWidget()
        self.w_result_panel = ResultPanelWidget()
        
        self.layout_LeftPanel.replaceWidget(self.ControlsWidgetPlaceholder, self.w_analyser_controls)
        self.layout_ResultPanel.replaceWidget(self.ResultPanelPlaceholder, self.w_result_panel)
        
        self.ControlsWidgetPlaceholder.setParent(None)
        self.ResultPanelPlaceholder.setParent(None)
        
        # Initiate services
        self.serv_analyser = AnalysisService()
        
        # Initiate presenters
        self.pres_analyser = PresenterAnalyser(
            controls=self.w_analyser_controls,
            result_panel=self.w_result_panel,
            analysis_service=self.serv_analyser,
        )

if __name__ == '__main__':
    import sys
    import pyqtgraph as pg
    
    from flashy.presenters.analyser import PresenterAnalyser
    
    pg.setConfigOptions(
        #leftButtonPan=False,
        foreground=(0, 0, 0, 255),
        background=(255, 255, 255, 255)
    )
    
    app = qtw.QApplication(sys.argv)
    
    tab = TabAnalyser()
    tab.show()
    
    sys.exit(app.exec())
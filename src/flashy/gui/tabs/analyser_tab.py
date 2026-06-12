from PySide6 import QtWidgets as qtw

from flashy.gui.ui.ui_analyser_tab import Ui_TabAnalyser
from flashy.gui.widgets.analyser_controls_widget import AnalyserControlsWidget
from flashy.gui.widgets.result_panel_widget import ResultPanelWidget

from flashy.services.analysis_service import AnalysisService
from flashy.presenters.analyser import PresenterAnalyser

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flashy.models.tree.node import TreeNode

class TabAnalyser(qtw.QWidget, Ui_TabAnalyser):
    def __init__(
        self, 
        root_node: "TreeNode",
        parent = None,
    ):
        super().__init__(parent)
        self.setupUi(self)
        self._root_node = root_node
        
        # Replace placeholder widgets with custom widgets
        self.w_analyser_controls = AnalyserControlsWidget(self._root_node)
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
    from flashy.models.tree.constructor import _make_test_config, construct_tree
    from flashy.gui.theme import FLASHy_THEME
    qtw.QApplication.setStyle("Fusion")
    
    root_node = construct_tree(_make_test_config())
    
    pg.setConfigOptions(
        #leftButtonPan=False,
        foreground=(0, 0, 0, 255),
        background=(255, 255, 255, 255)
    )
    
    app = qtw.QApplication(sys.argv)
    app.setPalette(FLASHy_THEME)
    
    tab = TabAnalyser(root_node)
    tab.show()
    
    sys.exit(app.exec())
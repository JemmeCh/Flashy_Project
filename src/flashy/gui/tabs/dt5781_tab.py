from PySide6 import QtWidgets as qtw

from flashy.gui.ui.ui_dt5781_tab import Ui_TabDT5781

from flashy.gui.widgets.feedback_widget import FeedbackWidget
from flashy.gui.widgets.dt5781_controls_widget import DT5781ControlsWidget
from flashy.gui.widgets.result_panel_widget import ResultPanelWidget

class TabDT5781(qtw.QWidget, Ui_TabDT5781):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
        # Replace placeholder widgets with custom widgets
        self.w_dt5781_controls = DT5781ControlsWidget()
        self.w_result_panel = ResultPanelWidget()
        
        self.layout_LeftPanel.replaceWidget(self.ControlsWidgetPlaceholder, self.w_dt5781_controls)
        self.layout_ResultPanel.replaceWidget(self.ResultPanelPlaceholder, self.w_result_panel)
        
        self.ControlsWidgetPlaceholder.setParent(None)
        self.ResultPanelPlaceholder.setParent(None)
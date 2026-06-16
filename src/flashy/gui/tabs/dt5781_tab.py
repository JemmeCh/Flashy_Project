from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from flashy.gui.ui.ui_dt5781_tab import Ui_TabDT5781
from flashy.gui.widgets.dt5781_controls_widget import DT5781ControlsWidget
from flashy.gui.widgets.result_panel_widget import ResultPanelWidget

from flashy.presenters.dt5781 import PresenterDT5781

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flashy.app_context import AppContext

class TabDT5781(qtw.QWidget, Ui_TabDT5781):
    def __init__(
        self, 
        app_context: "AppContext",
        parent = None,
    ):
        super().__init__(parent)
        self.setupUi(self)
        
        # Replace placeholder widgets with custom widgets
        self.w_dt5781_controls = DT5781ControlsWidget(app_context)
        self.w_result_panel = ResultPanelWidget()
        
        self.layout_LeftPanel.replaceWidget(self.ControlsWidgetPlaceholder, self.w_dt5781_controls)
        self.layout_ResultPanel.replaceWidget(self.ResultPanelPlaceholder, self.w_result_panel)
        
        self.ControlsWidgetPlaceholder.setParent(None)
        self.ResultPanelPlaceholder.setParent(None)
        
        # Initiate presenter + connections
        self.pres_dt5781 = PresenterDT5781(app_context)
        # Acquisition
        self.w_dt5781_controls.start_acquisition.connect(
            self.pres_dt5781.start_acquisition
        )
        self.w_dt5781_controls.stop_acquisition.connect(
            self.pres_dt5781.stop_acquisition
        )
        # State
        self.pres_dt5781.state_changed.connect(
            self.w_dt5781_controls.state_changed
        )
        # Set enabled
        self.pres_dt5781.send_set_enable_controls.connect(
            self.w_dt5781_controls.set_enabled_controls
        )
        self.pres_dt5781.send_set_enable_results.connect(
            self.w_result_panel.set_enabled_results
        )
        # Result update
        self.pres_dt5781.send_new_results.connect(
            self.w_result_panel.change_results
        )

if __name__ == '__main__':
    import sys
    
    from flashy.gui.theme import FLASHy_THEME
    from flashy.app_context import AppContext
    qtw.QApplication.setStyle("Fusion")
    
    app_context = AppContext()
    
    app = qtw.QApplication(sys.argv)
    app.setPalette(FLASHy_THEME)
    
    tab = TabDT5781(app_context)
    tab.show()
    
    sys.exit(app.exec())
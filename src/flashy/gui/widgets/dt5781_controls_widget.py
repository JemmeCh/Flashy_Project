from PySide6 import QtWidgets as qtw

from flashy.gui.ui.ui_dt5781_controls import Ui_DT5781ControlsWidget
from flashy.gui.treeview.parameter_treeview import ParameterTreeView

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flashy.models.tree.node import TreeNode

class DT5781ControlsWidget(qtw.QWidget, Ui_DT5781ControlsWidget):
    def __init__(
        self,
        root_node: "TreeNode", 
        parent=None
    ):
        super().__init__(parent)
        self.setupUi(self)
        self._root_node = root_node
        
        # Replace placeholder with custom widgets
        self.tv_parameters = ParameterTreeView(self._root_node)
        self.layout_Parameters.replaceWidget(self.ParameterTreeViewPlaceholder, self.tv_parameters)
        self.ParameterTreeViewPlaceholder.setParent(None)


if __name__ == '__main__':
    import sys
    from flashy.models.tree.constructor import _make_test_config, construct_tree
    from flashy.gui.widgets.analyser_controls_widget import AnalyserControlsWidget
    from flashy.gui.theme import FLASHy_THEME
    qtw.QApplication.setStyle("Fusion")
    
    root_node = construct_tree(_make_test_config())
    
    app = qtw.QApplication(sys.argv)
    app.setPalette(FLASHy_THEME)
    
    wid = qtw.QWidget()
    layout = qtw.QHBoxLayout()  # Horizontal = side-by-side
    w1 = DT5781ControlsWidget(root_node)
    w2 = AnalyserControlsWidget(root_node)
    
    layout.addWidget(w1)
    layout.addWidget(w2)
    
    wid.setLayout(layout)
    wid.show()
    
    sys.exit(app.exec())
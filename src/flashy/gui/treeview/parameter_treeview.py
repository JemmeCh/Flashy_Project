from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from flashy.gui.ui.ui_parameter_treeview import Ui_ParameterTreeView
from flashy.models.tree.model import ParameterTreeModel
from flashy.models.tree.delegate import ParameterDelegate

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flashy.models.tree.node import TreeNode

class ParameterTreeView(qtw.QWidget, Ui_ParameterTreeView):
    def __init__(
        self,
        root_node: "TreeNode", 
        parent=None
    ) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self._root_node = root_node
        self._param_model = ParameterTreeModel(self._root_node)
        self._delegate = ParameterDelegate()
        
        # Setup parameter view
        self.tv_parameters.setItemDelegateForColumn(1, self._delegate)
        self.tv_parameters.setModel(self._param_model)
        self.tv_parameters.expandAll()
        self.tv_parameters.header().setSectionResizeMode(qtw.QHeaderView.ResizeMode.ResizeToContents)
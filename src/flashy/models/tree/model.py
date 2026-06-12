from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from typing import TYPE_CHECKING, Any, override
if TYPE_CHECKING:
    from flashy.models.tree.node import TreeNode

class ParameterTreeModel(qtc.QAbstractItemModel):
    def __init__(self, root_node):
        super().__init__()
        self._root: "TreeNode" = root_node
        
        self._headers = [
            "Parameter Name",
            "Value",
            "Status"
        ]
    
    @override
    def rowCount(self, /, parent: qtc.QModelIndex | qtc.QPersistentModelIndex = qtc.QModelIndex()) -> int:
        if not parent.isValid():
            parent_node = self._root
        else:
            parent_node = parent.internalPointer()
        return parent_node.child_count()
    
    @override
    def columnCount(self, /, parent: qtc.QModelIndex | qtc.QPersistentModelIndex = qtc.QModelIndex()) -> int:
        # TODO:
        # - description column
        # - units column
        # - status column (hardware sync)
        return 3
    
    @override
    def index(self, row: int, column: int, /, parent: qtc.QModelIndex | qtc.QPersistentModelIndex = qtc.QModelIndex()) -> qtc.QModelIndex:
        if not parent.isValid():
            parent_node = self._root
        else:
            parent_node = parent.internalPointer()
            if parent_node is None: return qtc.QModelIndex()
        node = parent_node.child(row)
        if node: return self.createIndex(row, column, node)
        else: return qtc.QModelIndex()
    
    @override
    def parent(self, child: qtc.QModelIndex | qtc.QPersistentModelIndex) -> qtc.QModelIndex: #type:ignore
        if not child.isValid():
            node = self._root
        else: 
            node = child.internalPointer()
            if node is None: return qtc.QModelIndex()
        parent_node = node.parent
        if parent_node is None:
            return qtc.QModelIndex()
        return self.createIndex(parent_node.row(), 0, parent_node)
    
    @override
    def headerData(self, section: int, orientation: qtc.Qt.Orientation, /, role: int) -> Any: #type:ignore
        if role != qtc.Qt.ItemDataRole.DisplayRole:
            return None
        
        if orientation == qtc.Qt.Orientation.Horizontal:
            return self._headers[section]
    
    @override
    def data(self, index: qtc.QModelIndex | qtc.QPersistentModelIndex, /, role: int) -> Any: #type:ignore
        if not index.isValid():
            return None
        
        node = index.internalPointer()
        row = index.row()
        column = index.column()
        
        if role == qtc.Qt.ItemDataRole.DisplayRole:
            if column == 0: return node.display_name()
            elif column == 1: 
                if node.is_parameter: return node.get_value()
                else: return ''
            else: return None
        elif role == qtc.Qt.ItemDataRole.ToolTipRole:
            if node.is_parameter: return node.description()
            else: return None
        else:
            return None
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from flashy.services.logger.logger_service import get_logger

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
        
        self._logger = get_logger()
    
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
    def flags(self, index: qtc.QModelIndex | qtc.QPersistentModelIndex) -> qtc.Qt.ItemFlag:
        if not index.isValid():
            return qtc.Qt.ItemFlag.NoItemFlags
        
        col = index.column()
        node = index.internalPointer()
        if col != 1 or not node.is_parameter:
            return (
                qtc.Qt.ItemFlag.ItemIsSelectable
                | qtc.Qt.ItemFlag.ItemIsEnabled
            )
        
        return (
            qtc.Qt.ItemFlag.ItemIsSelectable
            | qtc.Qt.ItemFlag.ItemIsEnabled
            | qtc.Qt.ItemFlag.ItemIsEditable
        )
    
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
        
        if role == qtc.Qt.ItemDataRole.DisplayRole or role == qtc.Qt.ItemDataRole.EditRole:
            if column == 0: return node.display_name()
            elif column == 1: 
                if node.is_parameter: return node.get_value()
                else: return ''
            else: return None
        elif role == qtc.Qt.ItemDataRole.ToolTipRole:
            if node.is_parameter and column == 0: return node.description()
            else: return None
        else:
            return None
    
    @override
    def setData(self, index: qtc.QModelIndex | qtc.QPersistentModelIndex, value: Any, /, role: int) -> bool: #type:ignore
        if not index.isValid():
            return False
        node = index.internalPointer()
        if node.is_parameter:
            if node.get_value() == value:
                return False
            try:                
                node.set_value(value)
                self.dataChanged.emit(index, index, [qtc.Qt.ItemDataRole.EditRole])
                self._logger.info(f"Parameter '{node.name}' set to '{value}'.")
                return True
            except Exception as e:
                self._logger.warning(str(e))
                return False
        else: return False
    
    
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from flashy.services.logger.logger_service import get_logger

from typing import TYPE_CHECKING, Any, override
if TYPE_CHECKING:
    from flashy.models.tree.node import TreeNode

class ParameterTreeModel(qtc.QAbstractItemModel):
    """
    Qt model exposing a hierarchical parameter tree to Qt item views.
    
    This model adapts a :class:`TreeNode` hierarchy into a Qt-compatible
    item model, allowing parameter groups, containers, and leaf parameters
    to be displayed and edited in views such as QTreeView.
    
    It supports:
    
        - Hierarchical navigation (parent/child relationships)
        - Editable parameter values
        - Checkbox, editable, and read-only widgets
        - Tooltips for parameter descriptions
    
    :inherits: PySide6.QtCore.QAbstractItemModel
    """
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
        # - status column (hardware sync)
        return len(self._headers)
    
    @override
    def index(self, row: int, column: int, /, parent: qtc.QModelIndex | qtc.QPersistentModelIndex = qtc.QModelIndex()) -> qtc.QModelIndex:
        """
        Create an index for a given row, column, and parent.
        
        :param row: Row index within parent.
        :type row: int
        :param column: Column index.
        :type column: int
        :param parent: Parent index.
        :returns: Qt model index representing the node.
        :rtype: QModelIndex
        """
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
        """
        Return the parent index of a given child index.
        
        :param child: Child index.
        :returns: Parent index or invalid index if root.
        :rtype: QModelIndex
        """
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
        """
        Return item flags for a given index. 
        
        :param index: Model index.
        :returns: Qt item flags.
        :rtype: Qt.ItemFlag
        """
        if not index.isValid():
            return qtc.Qt.ItemFlag.NoItemFlags
        
        col = index.column()
        node = index.internalPointer()
        if col != 1 or not node.is_parameter:
            return (
                qtc.Qt.ItemFlag.ItemIsSelectable
                | qtc.Qt.ItemFlag.ItemIsEnabled
            )
        elif node.definition.widget_type == 'checkbox':
            return (
                qtc.Qt.ItemFlag.ItemIsUserCheckable
                | qtc.Qt.ItemFlag.ItemIsEnabled
                | qtc.Qt.ItemFlag.ItemIsSelectable
            )
        elif node.definition.widget_type == 'readonly':
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
        """
        Return header labels for the model.
        
        :param section: Column index.
        :type section: int
        :param orientation: Header orientation.
        :type orientation: Qt.Orientation
        :param role: Data role.
        :type role: int
        :returns: Header label or None.
        """
        if role != qtc.Qt.ItemDataRole.DisplayRole:
            return None
        
        if orientation == qtc.Qt.Orientation.Horizontal:
            return self._headers[section]
    
    @override
    def data(self, index: qtc.QModelIndex | qtc.QPersistentModelIndex, /, role: int) -> Any: #type:ignore
        """
        Return data for a given index and role.
        
        :param index: Model index.
        :type index: QModelIndex
        :param role: Data role requested by the view.
        :type role: int
        :returns: Role-dependent data or None.
        """
        if not index.isValid():
            return None
        
        node = index.internalPointer()
        row = index.row()
        column = index.column()
        
        if column == 1 and node.is_parameter and node.definition.widget_type == "checkbox":
            if role == qtc.Qt.ItemDataRole.CheckStateRole:
                return (
                    qtc.Qt.CheckState.Checked
                    if node.get_value()
                    else qtc.Qt.CheckState.Unchecked
                )
            elif role in (
                qtc.Qt.ItemDataRole.DisplayRole,
                qtc.Qt.ItemDataRole.EditRole,
            ):
                return None
        elif role in (
            qtc.Qt.ItemDataRole.DisplayRole,
            qtc.Qt.ItemDataRole.EditRole,
        ):
            if column == 0:
                return node.display_name()
            elif column == 1:
                return node.get_value() if node.is_parameter else ""
        elif role == qtc.Qt.ItemDataRole.ToolTipRole:
            if node.is_parameter and column == 0: return node.description()
            else: return None
        else:
            return None
    
    @override
    def setData(self, index: qtc.QModelIndex | qtc.QPersistentModelIndex, value: Any, /, role: int) -> bool: #type:ignore
        """
        Set the value of a parameter in the model.
        
        Updates the underlying :class:`TreeNode` value and emits change
        notifications to update the Qt view.
        
        :param index: Model index.
        :type index: QModelIndex
        :param value: New value to assign.
        :type value: Any
        :param role: Data role triggering the update.
        :type role: int
        :returns: True if the value was successfully updated, False otherwise.
        :rtype: bool
        """
        if not index.isValid():
            return False
        node = index.internalPointer()
        if node.is_parameter:
            if node.get_value() == value:
                return False
            try:
                node.set_value(value)
                if role == qtc.Qt.ItemDataRole.CheckStateRole:
                    value = "True" if value == 2 else "False"
                self.dataChanged.emit(index, index, [qtc.Qt.ItemDataRole.EditRole])
                self._logger.info(f"Parameter '{node.name}' set to '{value}'.")
                return True
            except Exception as e:
                self._logger.warning(str(e))
                return False
        else: return False
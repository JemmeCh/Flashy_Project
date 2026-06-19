from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from flashy.models.tree.node import TreeNode

from typing import TYPE_CHECKING, Any, override

class ParameterDelegate(qtw.QStyledItemDelegate):
    def __init__(
        self, 
        /, 
        parent: qtc.QObject | None = None
    ) -> None:
        super().__init__(parent)
    
    @override
    def createEditor(self, parent: qtw.QWidget, option: qtw.QStyleOptionViewItem, index: qtc.QModelIndex | qtc.QPersistentModelIndex) -> qtw.QWidget:
        if not index.isValid():
            return super().createEditor(parent, option, index)
        node = index.internalPointer()
        if not isinstance(node, TreeNode):
            return super().createEditor(parent, option, index)
        if not node.is_parameter:
            return super().createEditor(parent, option, index)
        assert node.definition
        assert node.container
        
        if index.column() == 1:
            if node.definition.widget_type == 'combobox':
                widget = qtw.QComboBox(parent)
            elif node.definition.widget_type == 'entry':
                if node.definition.parser:
                    widget = qtw.QLineEdit(parent)
                elif isinstance(node.definition.value_type, float):
                    widget = qtw.QDoubleSpinBox(parent)
                elif isinstance(node.definition.value_type, int):
                    widget = qtw.QSpinBox(parent)
                else:
                    widget = super().createEditor(parent, option, index)
            else: 
                widget = super().createEditor(parent, option, index)
            return widget
        else:
            return super().createEditor(parent, option, index)
    
    @override
    def setEditorData(self, editor: qtw.QWidget, index: qtc.QModelIndex | qtc.QPersistentModelIndex) -> None:
        if not index.isValid():
            return super().setEditorData(editor, index)
        node = index.internalPointer()
        if not isinstance(node, TreeNode):
            return super().setEditorData(editor, index)
        if not node.is_parameter:
            return super().setEditorData(editor, index)
        assert node.definition
        assert node.container
        
        value = node.get_value()
        if isinstance(editor, qtw.QComboBox):
            choices = node.definition.choices
            assert choices
            
            editor.insertItems(0, choices)
            editor.setCurrentText(str(value))
        elif isinstance(editor, qtw.QLineEdit):
            editor.setText(str(value))
        elif isinstance(editor, qtw.QSpinBox):
            valid_range = node.definition.valid_range
            step = node.definition.step
            if valid_range:
                editor.setRange(int(valid_range[0]), int(valid_range[1]))
            if step:
                editor.stepBy(int(step))
            
            editor.setValue(value) # type:ignore
        elif isinstance(editor, qtw.QDoubleSpinBox):
            valid_range = node.definition.valid_range
            step = node.definition.step
            if valid_range:
                editor.setRange(valid_range[0], valid_range[1])
            if step:
                editor.setStepType(qtw.QAbstractSpinBox.StepType.AdaptiveDecimalStepType)
                editor.stepBy(step) # type:ignore
            
            editor.setValue(value) # type:ignore
        else:
            super().setEditorData(editor, index)
    
    @override
    def setModelData(self, editor: qtw.QWidget, model: qtc.QAbstractItemModel, index: qtc.QModelIndex | qtc.QPersistentModelIndex) -> None:
        return super().setModelData(editor, model, index)
    
    @override
    def updateEditorGeometry(self, editor: qtw.QWidget, option: qtw.QStyleOptionViewItem, index: qtc.QModelIndex | qtc.QPersistentModelIndex) -> None:
        return super().updateEditorGeometry(editor, option, index)
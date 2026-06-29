from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw

from typing import override

class FileSystemModel(qtw.QFileSystemModel):
    """
    Custom QFileSystemModel that provides tooltip behavior on mouse hover.
    
    :inherits: PySide6.QtWidgets.QFileSystemModel
    """
    @override
    def data(self, index, role=qtc.Qt.ItemDataRole.DisplayRole): #type:ignore
        if role == qtc.Qt.ItemDataRole.ToolTipRole:
            return self.fileName(index)
        return super().data(index, role)
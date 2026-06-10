from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw

class FileSystemModel(qtw.QFileSystemModel):
    def data(self, index, role=qtc.Qt.ItemDataRole.DisplayRole): #type:ignore
        if role == qtc.Qt.ItemDataRole.ToolTipRole:
            return self.fileName(index)
        return super().data(index, role)
from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from typing import override


class ResultTableModel(qtc.QAbstractTableModel):
    def __init__(self, rows):
        super().__init__()
        
        # NOTE: The header should be a subclass of QHeaderView for N channels
        # But this should suffice for now
        self._headers = [
            "CH0\nCharge (nC)",
            "CH0\nDose (cGy)",
            "CH1\nCharge (nC)",
            "CH1\nDose (cGy)",
        ]
        
        self._rows = list(rows) if rows else [[0,0,0,0]]
        if self._rows:
            totals = [
                    sum(r[0] for r in self._rows),
                    sum(r[1] for r in self._rows),
                    sum(r[2] for r in self._rows),
                    sum(r[3] for r in self._rows),
                ]
            self._rows.append(totals)
    
    @override
    def rowCount(self, parent=None):
        if self._rows: return len(self._rows)
        else: return 0
    
    @override
    def columnCount(self, parent=None):
        return len(self._headers)
    
    @override
    def headerData(self, section: int, orientation: qtc.Qt.Orientation, role: int): #type:ignore
        if role != qtc.Qt.ItemDataRole.DisplayRole:
            return None
        
        if orientation == qtc.Qt.Orientation.Horizontal:
            return self._headers[section]
        elif orientation == qtc.Qt.Orientation.Vertical:
            if section == len(self._rows) - 1:
                return 'T'
            return str(section + 1)
    
    @override
    def data(self, index: qtc.QModelIndex, role=qtc.Qt.ItemDataRole.DisplayRole): #type:ignore
        if not index.isValid():
            return None
        elif role == qtc.Qt.ItemDataRole.DisplayRole:
            return self._rows[index.row()][index.column()]
        elif role == qtc.Qt.ItemDataRole.TextAlignmentRole:
            return qtc.Qt.AlignmentFlag.AlignCenter
        
        if self._rows and index.row() == len(self._rows) - 1:
            if role == qtc.Qt.ItemDataRole.BackgroundRole:
                return qtg.QBrush(qtc.Qt.GlobalColor.lightGray)
            elif role == qtc.Qt.ItemDataRole.FontRole:
                font = qtg.QFont()
                font.setBold(True)
                return font
    
    def set_rows(self, rows):
        self.beginResetModel()
        self._rows = rows.tolist() if rows is not None else []
        
        if self._rows:
            totals = [
                sum(r[0] for r in self._rows),
                sum(r[1] for r in self._rows),
                sum(r[2] for r in self._rows),
                sum(r[3] for r in self._rows),
            ]
            self._rows.append(totals)
        
        self.endResetModel()

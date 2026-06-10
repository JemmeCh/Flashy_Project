from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from flashy.models.result_table import ResultTableModel
from flashy.gui.ui.ui_result_table import Ui_ResultTable

class ResultTableView(qtw.QWidget, Ui_ResultTable):
    def __init__(self, data=None, parent=None,):
        super().__init__(parent)
        self.setupUi(self)
        
        # Setting up model
        self.model = ResultTableModel(data)
        self.tv_results.setModel(self.model)
        
        # Fixed + filling horizontal header
        header = self.tv_results.horizontalHeader()
        header.setSectionResizeMode(qtw.QHeaderView.ResizeMode.Stretch)
        self.tv_results.verticalHeader().setSectionResizeMode(qtw.QHeaderView.ResizeMode.Fixed)


if __name__ == '__main__':
    import sys
    import pyqtgraph as pg
    
    pg.setConfigOptions(
        #leftButtonPan=False,
        foreground=(0, 0, 0, 255),
        background=(255, 255, 255, 255)
    )
    
    data = [
        [0.3, 2, 0.2, 2.1],
        [0.2, 1.2, 0.3, 3]
    ]
    
    app = qtw.QApplication(sys.argv)
    
    tab = ResultTableView(data=data)
    tab.show()
    
    sys.exit(app.exec())
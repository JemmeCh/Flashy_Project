import os

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from flashy.gui.ui.ui_analyser_controls import Ui_AnalyserControlsWidget
from flashy.models.file_system import FileSystemModel
from flashy.models.tree.model import ParameterTreeModel
from flashy.models.tree.constructor import _make_test_config, construct_tree
from flashy.gui.theme import FLASHy_THEME
from flashy.services.logger.logger_service import get_logger

class AnalyserControlsWidget(qtw.QWidget, Ui_AnalyserControlsWidget):
    pressed_analyse_file = qtc.Signal(str)
    pressed_root_directory = qtc.Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self._logger = get_logger()
        
        # Setup tree view
        self.file_model = FileSystemModel()
        icon_provider = qtw.QFileIconProvider()
        self.file_model.setIconProvider(icon_provider)
        self.file_model.setRootPath("")
        self.tv_root_dir.setModel(self.file_model)
        self.change_treeview()
        self.tv_root_dir.setColumnWidth(0, 160)
        self.tv_root_dir.setColumnWidth(1, 60)
        self.tv_root_dir.setColumnHidden(2, True)
        self.tv_root_dir.setColumnHidden(3, True)
        self.tv_root_dir.header().setSectionResizeMode(qtw.QHeaderView.ResizeMode.ResizeToContents)
        
        # Setup parameter view
        # TODO: Fetch disk config
        self.root_node = construct_tree(_make_test_config())
        self.param_model = ParameterTreeModel(self.root_node)
        self.tv_parameters.setModel(self.param_model)
        self.tv_parameters.expandAll()
        self.tv_parameters.header().setSectionResizeMode(qtw.QHeaderView.ResizeMode.ResizeToContents)
        
        # Connections
        self.pb_root_directory.clicked.connect(self.change_root_directory)
        self.pb_analyse.clicked.connect(self.analyse_file)
        self.tv_root_dir.clicked.connect(self.select_file)
        
        self.tv_root_dir.setPalette(FLASHy_THEME)
    
    def change_treeview(self, new_root: str | None = None):
        if new_root:
            root_index = self.file_model.index(qtc.QDir.cleanPath(new_root))
        else:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            root_index = self.file_model.index(qtc.QDir.cleanPath(dir_path))
        
        if not root_index.isValid(): 
            raise ValueError(f"New root is invalid ({str(root_index)})")
        
        self.tv_root_dir.setRootIndex(root_index)
        self._logger.info(f"Directory changed to {new_root}")
    
    
    @qtc.Slot()
    def change_root_directory(self):
        dialog = qtw.QFileDialog()
        dialog.setFileMode(qtw.QFileDialog.FileMode.Directory)
        if dialog.exec():
            try:
                self.change_treeview(dialog.selectedFiles()[0])
            except Exception as e:
                self._logger.exception("Failed to change root directory")
    
    @qtc.Slot()
    def select_file(self):
        selected = self.tv_root_dir.selectedIndexes()[0]
        self.full_file_path = self.file_model.filePath(selected)
        self.filename = self.file_model.fileName(selected)
        self.le_selected_file.setText(self.filename)
    
    @qtc.Slot()
    def analyse_file(self):
        if not hasattr(self, "full_file_path"):
            self._logger.warning("No file selected")
            return
        self.pressed_analyse_file.emit(self.full_file_path)


if __name__ == '__main__':
    import sys
    qtw.QApplication.setStyle("Fusion")
    
    app = qtw.QApplication(sys.argv)
    app.setPalette(FLASHy_THEME)
    
    w = AnalyserControlsWidget()
    w.show()
    sys.exit(app.exec())
import os

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from flashy.gui.ui.ui_analyser_controls import Ui_AnalyserControlsWidget
from flashy.gui.treeview.parameter_treeview import ParameterTreeView
from flashy.models.file_system import FileSystemModel
from flashy.services.logger.logger_service import get_logger

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from flashy.app_context import AppContext

class AnalyserControlsWidget(qtw.QWidget, Ui_AnalyserControlsWidget):
    pressed_analyse_file = qtc.Signal(str)
    pressed_root_directory = qtc.Signal()
    
    def __init__(
        self, 
        app_context: "AppContext", 
        parent=None
    ):
        super().__init__(parent)
        self.setupUi(self)
        self._logger = get_logger()
        self._user_config = app_context.user_config
        
        # Replace placeholder with custom widgets
        self.tv_parameters = ParameterTreeView(app_context.analyser_tree)
        self.layout_AnalyserParameters.replaceWidget(self.ParameterTreeViewPlaceholder, self.tv_parameters)
        self.ParameterTreeViewPlaceholder.setParent(None)
        
        self.le_selected_file.selectionChanged.connect(lambda: self.le_selected_file.setSelection(0, 0))
        
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
        
        # Internal connections
        self.pb_root_directory.clicked.connect(self.change_root_directory)
        self.pb_analyse.clicked.connect(self.analyse_file)
        self.tv_root_dir.clicked.connect(self.select_file)
    
    # ==========================
    # Helper Functions
    # ==========================
    
    def change_treeview(self, new_root: str | None = None):
        if new_root:
            root_index = self.file_model.index(qtc.QDir.cleanPath(new_root))
        else:
            new_root = self._user_config.get_value('analyser_root')
            if new_root == "Please choose a root path":
                root_index = self.file_model.index(qtc.QDir.cleanPath(__file__))
            else:
                root_index = self.file_model.index(qtc.QDir.cleanPath(new_root)) # type:ignore
        
        if not root_index.isValid(): 
            raise ValueError(f"New root is invalid ({str(root_index)})")
        
        self.tv_root_dir.setRootIndex(root_index)
        self.label_root.setText(f'Root: {new_root}')
        # TODO: Change this to proper model
        self._user_config.set_value('analyser_root', new_root)
        self._logger.info(f"Directory changed to: {new_root}")
    
    # ==========================
    # External Slots
    # ==========================
    
    @qtc.Slot()
    def analyse_file(self):
        if not hasattr(self, "full_file_path"):
            self._logger.warning("No file selected")
            return
        # TODO: Use self._user_config to put or not user analysis parameters
        # TODO: Make new (boolean) paramter in Analysis for this
        # TODO: Support for boolean parameters
        self.pressed_analyse_file.emit(self.full_file_path)
    
    # ==========================
    # Internal Slots
    # ==========================
    
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


if __name__ == '__main__':
    import sys
    from flashy.gui.theme import FLASHy_THEME
    from flashy.app_context import AppContext
    qtw.QApplication.setStyle("Fusion")
    
    app_context = AppContext()
    
    app = qtw.QApplication(sys.argv)
    app.setPalette(FLASHy_THEME)
    
    #wid = qtw.QWidget()
    #layout = qtw.QHBoxLayout()  # Horizontal = side-by-side
    w1 = AnalyserControlsWidget(app_context)
    #w2 = AnalyserControlsWidget(root_node)
    
    #layout.addWidget(w1)
    #layout.addWidget(w2)
    
    #wid.setLayout(layout)
    #wid.show()
    w1.show()
    
    sys.exit(app.exec())
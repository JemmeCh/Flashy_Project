import sys

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg


from flashy.app_context import AppContext
from flashy.gui.theme import FLASHy_THEME
from flashy.gui.main_window import MainWindow


def main() -> None:
    app_context = AppContext()
    qtw.QApplication.setStyle("Fusion")
    
    app = qtw.QApplication(sys.argv)
    app.setPalette(FLASHy_THEME)
    
    window = MainWindow(app_context)
    window.show()
    
    app.aboutToQuit.connect(window.on_quit)
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
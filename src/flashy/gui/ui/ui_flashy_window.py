# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'flashy_window.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QMainWindow, QMenu,
    QMenuBar, QSizePolicy, QStatusBar, QTabWidget,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 600)
        MainWindow.setMinimumSize(QSize(1000, 600))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(1, 1, 1, 1)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_analyser = QWidget()
        self.tab_analyser.setObjectName(u"tab_analyser")
        self.layout_TabAnalyser = QGridLayout(self.tab_analyser)
        self.layout_TabAnalyser.setSpacing(0)
        self.layout_TabAnalyser.setObjectName(u"layout_TabAnalyser")
        self.layout_TabAnalyser.setContentsMargins(0, 0, 0, 0)
        self.TabAnalyserPlaceholder = QWidget(self.tab_analyser)
        self.TabAnalyserPlaceholder.setObjectName(u"TabAnalyserPlaceholder")

        self.layout_TabAnalyser.addWidget(self.TabAnalyserPlaceholder, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_analyser, "")
        self.tab_dt5781 = QWidget()
        self.tab_dt5781.setObjectName(u"tab_dt5781")
        self.layout_TabDT5781 = QGridLayout(self.tab_dt5781)
        self.layout_TabDT5781.setSpacing(0)
        self.layout_TabDT5781.setObjectName(u"layout_TabDT5781")
        self.layout_TabDT5781.setContentsMargins(0, 0, 0, 0)
        self.TabDT5781Placeholder = QWidget(self.tab_dt5781)
        self.TabDT5781Placeholder.setObjectName(u"TabDT5781Placeholder")

        self.layout_TabDT5781.addWidget(self.TabDT5781Placeholder, 2, 2, 1, 1)

        self.tabWidget.addTab(self.tab_dt5781, "")
        self.tab_ADE = QWidget()
        self.tab_ADE.setObjectName(u"tab_ADE")
        self.layout_TabADE = QGridLayout(self.tab_ADE)
        self.layout_TabADE.setSpacing(0)
        self.layout_TabADE.setObjectName(u"layout_TabADE")
        self.layout_TabADE.setContentsMargins(0, 0, 0, 0)
        self.TabADEPlaceholder = QWidget(self.tab_ADE)
        self.TabADEPlaceholder.setObjectName(u"TabADEPlaceholder")

        self.layout_TabADE.addWidget(self.TabADEPlaceholder, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_ADE, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1000, 33))
        self.menuFiles = QMenu(self.menubar)
        self.menuFiles.setObjectName(u"menuFiles")
        self.menuAnalyse = QMenu(self.menubar)
        self.menuAnalyse.setObjectName(u"menuAnalyse")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuClose = QMenu(self.menubar)
        self.menuClose.setObjectName(u"menuClose")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFiles.menuAction())
        self.menubar.addAction(self.menuAnalyse.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menuClose.menuAction())

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"FLASHy", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_analyser), QCoreApplication.translate("MainWindow", u"Analyser", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_dt5781), QCoreApplication.translate("MainWindow", u"Caen DT5781", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_ADE), QCoreApplication.translate("MainWindow", u"Bergoz ADE", None))
        self.menuFiles.setTitle(QCoreApplication.translate("MainWindow", u"Files", None))
        self.menuAnalyse.setTitle(QCoreApplication.translate("MainWindow", u"Analyse", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuClose.setTitle(QCoreApplication.translate("MainWindow", u"Close", None))
    # retranslateUi


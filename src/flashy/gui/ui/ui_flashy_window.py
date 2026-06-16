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
        MainWindow.resize(1200, 800)
        MainWindow.setMinimumSize(QSize(1200, 800))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.layout_window = QGridLayout(self.centralwidget)
        self.layout_window.setSpacing(1)
        self.layout_window.setObjectName(u"layout_window")
        self.layout_window.setContentsMargins(1, 1, 1, 1)
        self.tab_holder = QTabWidget(self.centralwidget)
        self.tab_holder.setObjectName(u"tab_holder")
        self.tab_analyser = QWidget()
        self.tab_analyser.setObjectName(u"tab_analyser")
        self.layout_TabAnalyser = QGridLayout(self.tab_analyser)
        self.layout_TabAnalyser.setSpacing(0)
        self.layout_TabAnalyser.setObjectName(u"layout_TabAnalyser")
        self.layout_TabAnalyser.setContentsMargins(0, 0, 0, 0)
        self.TabAnalyserPlaceholder = QWidget(self.tab_analyser)
        self.TabAnalyserPlaceholder.setObjectName(u"TabAnalyserPlaceholder")

        self.layout_TabAnalyser.addWidget(self.TabAnalyserPlaceholder, 0, 0, 1, 1)

        self.tab_holder.addTab(self.tab_analyser, "")
        self.tab_dt5781 = QWidget()
        self.tab_dt5781.setObjectName(u"tab_dt5781")
        self.layout_TabDT5781 = QGridLayout(self.tab_dt5781)
        self.layout_TabDT5781.setSpacing(0)
        self.layout_TabDT5781.setObjectName(u"layout_TabDT5781")
        self.layout_TabDT5781.setContentsMargins(0, 0, 0, 0)
        self.TabDT5781Placeholder = QWidget(self.tab_dt5781)
        self.TabDT5781Placeholder.setObjectName(u"TabDT5781Placeholder")

        self.layout_TabDT5781.addWidget(self.TabDT5781Placeholder, 2, 2, 1, 1)

        self.tab_holder.addTab(self.tab_dt5781, "")
        self.tab_ADE = QWidget()
        self.tab_ADE.setObjectName(u"tab_ADE")
        self.layout_TabADE = QGridLayout(self.tab_ADE)
        self.layout_TabADE.setSpacing(0)
        self.layout_TabADE.setObjectName(u"layout_TabADE")
        self.layout_TabADE.setContentsMargins(0, 0, 0, 0)
        self.TabADEPlaceholder = QWidget(self.tab_ADE)
        self.TabADEPlaceholder.setObjectName(u"TabADEPlaceholder")

        self.layout_TabADE.addWidget(self.TabADEPlaceholder, 0, 0, 1, 1)

        self.tab_holder.addTab(self.tab_ADE, "")

        self.layout_window.addWidget(self.tab_holder, 0, 0, 1, 1)

        self.FeedbackPlaceholder = QWidget(self.centralwidget)
        self.FeedbackPlaceholder.setObjectName(u"FeedbackPlaceholder")
        self.FeedbackPlaceholder.setMinimumSize(QSize(0, 200))

        self.layout_window.addWidget(self.FeedbackPlaceholder, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1200, 33))
        self.menuFiles = QMenu(self.menubar)
        self.menuFiles.setObjectName(u"menuFiles")
        self.menuAnalyse = QMenu(self.menubar)
        self.menuAnalyse.setObjectName(u"menuAnalyse")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName(u"menuHelp")
        self.menuClose = QMenu(self.menubar)
        self.menuClose.setObjectName(u"menuClose")
        MainWindow.setMenuBar(self.menubar)
        self.status_bar = QStatusBar(MainWindow)
        self.status_bar.setObjectName(u"status_bar")
        MainWindow.setStatusBar(self.status_bar)

        self.menubar.addAction(self.menuFiles.menuAction())
        self.menubar.addAction(self.menuAnalyse.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menubar.addAction(self.menuClose.menuAction())

        self.retranslateUi(MainWindow)

        self.tab_holder.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"FLASHy", None))
        self.tab_holder.setTabText(self.tab_holder.indexOf(self.tab_analyser), QCoreApplication.translate("MainWindow", u"Analyser", None))
        self.tab_holder.setTabText(self.tab_holder.indexOf(self.tab_dt5781), QCoreApplication.translate("MainWindow", u"Caen DT5781", None))
        self.tab_holder.setTabText(self.tab_holder.indexOf(self.tab_ADE), QCoreApplication.translate("MainWindow", u"Bergoz ADE", None))
        self.menuFiles.setTitle(QCoreApplication.translate("MainWindow", u"Files", None))
        self.menuAnalyse.setTitle(QCoreApplication.translate("MainWindow", u"Analyse", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
        self.menuClose.setTitle(QCoreApplication.translate("MainWindow", u"Close", None))
    # retranslateUi


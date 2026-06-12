# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'analyser_tab.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_TabAnalyser(object):
    def setupUi(self, TabAnalyser):
        if not TabAnalyser.objectName():
            TabAnalyser.setObjectName(u"TabAnalyser")
        TabAnalyser.resize(943, 390)
        self.gridLayout = QGridLayout(TabAnalyser)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
        self.line = QFrame(TabAnalyser)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 0, 1, 1, 1)

        self.LeftPanel = QWidget(TabAnalyser)
        self.LeftPanel.setObjectName(u"LeftPanel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LeftPanel.sizePolicy().hasHeightForWidth())
        self.LeftPanel.setSizePolicy(sizePolicy)
        self.LeftPanel.setMinimumSize(QSize(500, 0))
        self.layout_LeftPanel = QVBoxLayout(self.LeftPanel)
        self.layout_LeftPanel.setSpacing(0)
        self.layout_LeftPanel.setObjectName(u"layout_LeftPanel")
        self.layout_LeftPanel.setContentsMargins(0, 0, 0, 0)
        self.ControlsWidgetPlaceholder = QWidget(self.LeftPanel)
        self.ControlsWidgetPlaceholder.setObjectName(u"ControlsWidgetPlaceholder")

        self.layout_LeftPanel.addWidget(self.ControlsWidgetPlaceholder)


        self.gridLayout.addWidget(self.LeftPanel, 0, 0, 1, 1)

        self.ResultPanel = QWidget(TabAnalyser)
        self.ResultPanel.setObjectName(u"ResultPanel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.ResultPanel.sizePolicy().hasHeightForWidth())
        self.ResultPanel.setSizePolicy(sizePolicy1)
        self.layout_ResultPanel = QGridLayout(self.ResultPanel)
        self.layout_ResultPanel.setSpacing(0)
        self.layout_ResultPanel.setObjectName(u"layout_ResultPanel")
        self.layout_ResultPanel.setContentsMargins(0, 0, 0, 0)
        self.ResultPanelPlaceholder = QWidget(self.ResultPanel)
        self.ResultPanelPlaceholder.setObjectName(u"ResultPanelPlaceholder")

        self.layout_ResultPanel.addWidget(self.ResultPanelPlaceholder, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.ResultPanel, 0, 2, 1, 1)


        self.retranslateUi(TabAnalyser)

        QMetaObject.connectSlotsByName(TabAnalyser)
    # setupUi

    def retranslateUi(self, TabAnalyser):
        TabAnalyser.setWindowTitle(QCoreApplication.translate("TabAnalyser", u"TabAnalyser", None))
    # retranslateUi


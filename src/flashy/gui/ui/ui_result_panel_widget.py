# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'result_panel_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QSizePolicy, QWidget)

from pyqtgraph import PlotWidget

class Ui_ResultPanelWidget(object):
    def setupUi(self, ResultPanelWidget):
        if not ResultPanelWidget.objectName():
            ResultPanelWidget.setObjectName(u"ResultPanelWidget")
        ResultPanelWidget.resize(600, 400)
        self.layout_ResultPanel = QGridLayout(ResultPanelWidget)
        self.layout_ResultPanel.setSpacing(6)
        self.layout_ResultPanel.setObjectName(u"layout_ResultPanel")
        self.layout_ResultPanel.setContentsMargins(6, 6, 6, 6)
        self.graph_top = PlotWidget(ResultPanelWidget)
        self.graph_top.setObjectName(u"graph_top")

        self.layout_ResultPanel.addWidget(self.graph_top, 0, 0, 1, 1)

        self.ResultTablePlaceholder = QWidget(ResultPanelWidget)
        self.ResultTablePlaceholder.setObjectName(u"ResultTablePlaceholder")

        self.layout_ResultPanel.addWidget(self.ResultTablePlaceholder, 2, 1, 1, 1)

        self.graph_right = PlotWidget(ResultPanelWidget)
        self.graph_right.setObjectName(u"graph_right")

        self.layout_ResultPanel.addWidget(self.graph_right, 0, 1, 2, 1)

        self.graph_bot = PlotWidget(ResultPanelWidget)
        self.graph_bot.setObjectName(u"graph_bot")

        self.layout_ResultPanel.addWidget(self.graph_bot, 2, 0, 1, 1)


        self.retranslateUi(ResultPanelWidget)

        QMetaObject.connectSlotsByName(ResultPanelWidget)
    # setupUi

    def retranslateUi(self, ResultPanelWidget):
        ResultPanelWidget.setWindowTitle(QCoreApplication.translate("ResultPanelWidget", u"ResultPanelWidget", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'parameter_treeview.ui'
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QSizePolicy, QTreeView,
    QVBoxLayout, QWidget)

class Ui_ParameterTreeView(object):
    def setupUi(self, ParameterTreeView):
        if not ParameterTreeView.objectName():
            ParameterTreeView.setObjectName(u"ParameterTreeView")
        ParameterTreeView.resize(400, 300)
        self.verticalLayout = QVBoxLayout(ParameterTreeView)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tv_parameters = QTreeView(ParameterTreeView)
        self.tv_parameters.setObjectName(u"tv_parameters")
        self.tv_parameters.setAlternatingRowColors(True)
        self.tv_parameters.header().setMinimumSectionSize(10)
        self.tv_parameters.header().setDefaultSectionSize(10)

        self.verticalLayout.addWidget(self.tv_parameters)


        self.retranslateUi(ParameterTreeView)

        QMetaObject.connectSlotsByName(ParameterTreeView)
    # setupUi

    def retranslateUi(self, ParameterTreeView):
        ParameterTreeView.setWindowTitle(QCoreApplication.translate("ParameterTreeView", u"ParameterTreeView", None))
    # retranslateUi


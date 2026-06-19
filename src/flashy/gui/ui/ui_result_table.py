# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'result_table.ui'
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QTableView, QVBoxLayout, QWidget)

class Ui_ResultTable(object):
    def setupUi(self, ResultTable):
        if not ResultTable.objectName():
            ResultTable.setObjectName(u"ResultTable")
        ResultTable.resize(400, 302)
        self.verticalLayout = QVBoxLayout(ResultTable)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.l_title = QLabel(ResultTable)
        self.l_title.setObjectName(u"l_title")
        font = QFont()
        font.setPointSize(12)
        self.l_title.setFont(font)
        self.l_title.setTextFormat(Qt.TextFormat.AutoText)
        self.l_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.l_title)

        self.tv_results = QTableView(ResultTable)
        self.tv_results.setObjectName(u"tv_results")
        self.tv_results.setAlternatingRowColors(True)
        self.tv_results.setGridStyle(Qt.PenStyle.SolidLine)
        self.tv_results.horizontalHeader().setCascadingSectionResizes(True)
        self.tv_results.horizontalHeader().setMinimumSectionSize(1)
        self.tv_results.horizontalHeader().setDefaultSectionSize(70)
        self.tv_results.horizontalHeader().setStretchLastSection(True)
        self.tv_results.verticalHeader().setMinimumSectionSize(1)
        self.tv_results.verticalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.tv_results)

        self.pb_save_results = QPushButton(ResultTable)
        self.pb_save_results.setObjectName(u"pb_save_results")

        self.verticalLayout.addWidget(self.pb_save_results)


        self.retranslateUi(ResultTable)

        QMetaObject.connectSlotsByName(ResultTable)
    # setupUi

    def retranslateUi(self, ResultTable):
        ResultTable.setWindowTitle(QCoreApplication.translate("ResultTable", u"ResultTable", None))
        self.l_title.setText(QCoreApplication.translate("ResultTable", u"Charge and dose per channel", None))
        self.pb_save_results.setText(QCoreApplication.translate("ResultTable", u"Save Results", None))
    # retranslateUi


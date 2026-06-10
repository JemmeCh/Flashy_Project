# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'feedback_widget.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QFrame, QGridLayout,
    QGroupBox, QPlainTextEdit, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_FeedbackWidget(object):
    def setupUi(self, FeedbackWidget):
        if not FeedbackWidget.objectName():
            FeedbackWidget.setObjectName(u"FeedbackWidget")
        FeedbackWidget.resize(300, 200)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FeedbackWidget.sizePolicy().hasHeightForWidth())
        FeedbackWidget.setSizePolicy(sizePolicy)
        FeedbackWidget.setMinimumSize(QSize(0, 200))
        self.gridLayout = QGridLayout(FeedbackWidget)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(6, 6, 6, 6)
        self.Feedback = QGroupBox(FeedbackWidget)
        self.Feedback.setObjectName(u"Feedback")
        self.verticalLayout = QVBoxLayout(self.Feedback)
        self.verticalLayout.setSpacing(1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.plainTextEdit = QPlainTextEdit(self.Feedback)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setAcceptDrops(False)
        self.plainTextEdit.setFrameShape(QFrame.Shape.StyledPanel)
        self.plainTextEdit.setFrameShadow(QFrame.Shadow.Raised)
        self.plainTextEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.plainTextEdit.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.plainTextEdit.setReadOnly(True)

        self.verticalLayout.addWidget(self.plainTextEdit)


        self.gridLayout.addWidget(self.Feedback, 0, 0, 1, 1)


        self.retranslateUi(FeedbackWidget)

        QMetaObject.connectSlotsByName(FeedbackWidget)
    # setupUi

    def retranslateUi(self, FeedbackWidget):
        FeedbackWidget.setWindowTitle(QCoreApplication.translate("FeedbackWidget", u"FeedbackWidget", None))
        self.Feedback.setTitle(QCoreApplication.translate("FeedbackWidget", u"Feedback", None))
        self.plainTextEdit.setPlainText("")
        self.plainTextEdit.setPlaceholderText(QCoreApplication.translate("FeedbackWidget", u"Welcome to FLASHy!", None))
    # retranslateUi


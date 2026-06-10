# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dt5781_controls.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QGroupBox,
    QLCDNumber, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_DT5781ControlsWidget(object):
    def setupUi(self, DT5781ControlsWidget):
        if not DT5781ControlsWidget.objectName():
            DT5781ControlsWidget.setObjectName(u"DT5781ControlsWidget")
        DT5781ControlsWidget.resize(300, 386)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DT5781ControlsWidget.sizePolicy().hasHeightForWidth())
        DT5781ControlsWidget.setSizePolicy(sizePolicy)
        DT5781ControlsWidget.setMinimumSize(QSize(300, 0))
        self.verticalLayout = QVBoxLayout(DT5781ControlsWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(DT5781ControlsWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy1)
        self.tab_acquisition = QWidget()
        self.tab_acquisition.setObjectName(u"tab_acquisition")
        self.layout_tab = QVBoxLayout(self.tab_acquisition)
        self.layout_tab.setObjectName(u"layout_tab")
        self.layout_tab.setContentsMargins(6, 6, 6, 6)
        self.gb_project = QGroupBox(self.tab_acquisition)
        self.gb_project.setObjectName(u"gb_project")
        sizePolicy1.setHeightForWidth(self.gb_project.sizePolicy().hasHeightForWidth())
        self.gb_project.setSizePolicy(sizePolicy1)
        self.layout_project = QGridLayout(self.gb_project)
        self.layout_project.setObjectName(u"layout_project")
        self.layout_project.setContentsMargins(6, 6, 6, 6)
        self.line_2 = QFrame(self.gb_project)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.layout_project.addWidget(self.line_2, 2, 0, 1, 2)

        self.le_project = QLineEdit(self.gb_project)
        self.le_project.setObjectName(u"le_project")

        self.layout_project.addWidget(self.le_project, 0, 1, 1, 1)

        self.pb_shoot = QPushButton(self.gb_project)
        self.pb_shoot.setObjectName(u"pb_shoot")

        self.layout_project.addWidget(self.pb_shoot, 4, 0, 1, 2)

        self.le_next_shoot = QLineEdit(self.gb_project)
        self.le_next_shoot.setObjectName(u"le_next_shoot")
        self.le_next_shoot.setReadOnly(True)

        self.layout_project.addWidget(self.le_next_shoot, 6, 1, 1, 1)

        self.label_next_shoot = QLabel(self.gb_project)
        self.label_next_shoot.setObjectName(u"label_next_shoot")

        self.layout_project.addWidget(self.label_next_shoot, 6, 0, 1, 1)

        self.label_project = QLabel(self.gb_project)
        self.label_project.setObjectName(u"label_project")

        self.layout_project.addWidget(self.label_project, 0, 0, 1, 1)

        self.le_shoot = QLineEdit(self.gb_project)
        self.le_shoot.setObjectName(u"le_shoot")

        self.layout_project.addWidget(self.le_shoot, 3, 1, 1, 1)

        self.pb_project = QPushButton(self.gb_project)
        self.pb_project.setObjectName(u"pb_project")

        self.layout_project.addWidget(self.pb_project, 1, 0, 1, 2)

        self.label_shoot = QLabel(self.gb_project)
        self.label_shoot.setObjectName(u"label_shoot")

        self.layout_project.addWidget(self.label_shoot, 3, 0, 1, 1)

        self.line = QFrame(self.gb_project)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.layout_project.addWidget(self.line, 5, 0, 1, 2)


        self.layout_tab.addWidget(self.gb_project)

        self.line_3 = QFrame(self.tab_acquisition)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.layout_tab.addWidget(self.line_3)

        self.gb_digitizer = QGroupBox(self.tab_acquisition)
        self.gb_digitizer.setObjectName(u"gb_digitizer")
        self.layout_digitizer = QGridLayout(self.gb_digitizer)
        self.layout_digitizer.setObjectName(u"layout_digitizer")
        self.layout_digitizer.setContentsMargins(6, 6, 6, 6)
        self.le_status = QLineEdit(self.gb_digitizer)
        self.le_status.setObjectName(u"le_status")
        self.le_status.setReadOnly(True)

        self.layout_digitizer.addWidget(self.le_status, 0, 2, 1, 1)

        self.pb_acquisition = QPushButton(self.gb_digitizer)
        self.pb_acquisition.setObjectName(u"pb_acquisition")

        self.layout_digitizer.addWidget(self.pb_acquisition, 1, 0, 1, 3)

        self.label_status = QLabel(self.gb_digitizer)
        self.label_status.setObjectName(u"label_status")

        self.layout_digitizer.addWidget(self.label_status, 0, 0, 1, 1)

        self.LCDTimerPlaceholder = QLCDNumber(self.gb_digitizer)
        self.LCDTimerPlaceholder.setObjectName(u"LCDTimerPlaceholder")
        self.LCDTimerPlaceholder.setSmallDecimalPoint(False)
        self.LCDTimerPlaceholder.setDigitCount(9)
        self.LCDTimerPlaceholder.setProperty(u"value", 0.000000000000000)

        self.layout_digitizer.addWidget(self.LCDTimerPlaceholder, 2, 0, 1, 3)


        self.layout_tab.addWidget(self.gb_digitizer)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.layout_tab.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.tab_acquisition, "")
        self.tab_parameters = QWidget()
        self.tab_parameters.setObjectName(u"tab_parameters")
        self.gridLayout = QGridLayout(self.tab_parameters)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(6, 6, 6, 6)
        self.DT5781ParametersPlaceholder = QWidget(self.tab_parameters)
        self.DT5781ParametersPlaceholder.setObjectName(u"DT5781ParametersPlaceholder")

        self.gridLayout.addWidget(self.DT5781ParametersPlaceholder, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_parameters, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.retranslateUi(DT5781ControlsWidget)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(DT5781ControlsWidget)
    # setupUi

    def retranslateUi(self, DT5781ControlsWidget):
        DT5781ControlsWidget.setWindowTitle(QCoreApplication.translate("DT5781ControlsWidget", u"DT5781ControlsWidget", None))
        self.gb_project.setTitle(QCoreApplication.translate("DT5781ControlsWidget", u"Project", None))
        self.pb_shoot.setText(QCoreApplication.translate("DT5781ControlsWidget", u"Change Acquisition Name", None))
        self.label_next_shoot.setText(QCoreApplication.translate("DT5781ControlsWidget", u"Next Acquisition:", None))
        self.label_project.setText(QCoreApplication.translate("DT5781ControlsWidget", u"Current Project:", None))
        self.pb_project.setText(QCoreApplication.translate("DT5781ControlsWidget", u"Change Current Project", None))
        self.label_shoot.setText(QCoreApplication.translate("DT5781ControlsWidget", u"Acquisition Name:", None))
        self.gb_digitizer.setTitle(QCoreApplication.translate("DT5781ControlsWidget", u"Digitizer", None))
        self.pb_acquisition.setText(QCoreApplication.translate("DT5781ControlsWidget", u"Begin Acquisition", None))
        self.label_status.setText(QCoreApplication.translate("DT5781ControlsWidget", u"Status:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_acquisition), QCoreApplication.translate("DT5781ControlsWidget", u"Acquisition", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_parameters), QCoreApplication.translate("DT5781ControlsWidget", u"Parameters", None))
    # retranslateUi


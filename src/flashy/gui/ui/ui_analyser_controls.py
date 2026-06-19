# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'analyser_controls.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QGridLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QTabWidget, QTreeView, QVBoxLayout,
    QWidget)

class Ui_AnalyserControlsWidget(object):
    def setupUi(self, AnalyserControlsWidget):
        if not AnalyserControlsWidget.objectName():
            AnalyserControlsWidget.setObjectName(u"AnalyserControlsWidget")
        AnalyserControlsWidget.resize(496, 471)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AnalyserControlsWidget.sizePolicy().hasHeightForWidth())
        AnalyserControlsWidget.setSizePolicy(sizePolicy)
        AnalyserControlsWidget.setMinimumSize(QSize(300, 0))
        self.verticalLayout = QVBoxLayout(AnalyserControlsWidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(AnalyserControlsWidget)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy1)
        self.tab_file_selection = QWidget()
        self.tab_file_selection.setObjectName(u"tab_file_selection")
        self.layout = QFormLayout(self.tab_file_selection)
        self.layout.setObjectName(u"layout")
        self.layout.setContentsMargins(6, 6, 6, 6)
        self.line_top = QFrame(self.tab_file_selection)
        self.line_top.setObjectName(u"line_top")
        self.line_top.setFrameShape(QFrame.Shape.HLine)
        self.line_top.setFrameShadow(QFrame.Shadow.Sunken)

        self.layout.setWidget(1, QFormLayout.ItemRole.SpanningRole, self.line_top)

        self.tv_root_dir = QTreeView(self.tab_file_selection)
        self.tv_root_dir.setObjectName(u"tv_root_dir")
        self.tv_root_dir.setAlternatingRowColors(True)
        self.tv_root_dir.setIndentation(10)
        self.tv_root_dir.setItemsExpandable(True)
        self.tv_root_dir.header().setMinimumSectionSize(30)
        self.tv_root_dir.header().setDefaultSectionSize(100)

        self.layout.setWidget(3, QFormLayout.ItemRole.SpanningRole, self.tv_root_dir)

        self.line_bottom = QFrame(self.tab_file_selection)
        self.line_bottom.setObjectName(u"line_bottom")
        self.line_bottom.setFrameShape(QFrame.Shape.HLine)
        self.line_bottom.setFrameShadow(QFrame.Shadow.Sunken)

        self.layout.setWidget(4, QFormLayout.ItemRole.SpanningRole, self.line_bottom)

        self.label_selected = QLabel(self.tab_file_selection)
        self.label_selected.setObjectName(u"label_selected")

        self.layout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.label_selected)

        self.pb_root_directory = QPushButton(self.tab_file_selection)
        self.pb_root_directory.setObjectName(u"pb_root_directory")

        self.layout.setWidget(0, QFormLayout.ItemRole.SpanningRole, self.pb_root_directory)

        self.le_selected_file = QLineEdit(self.tab_file_selection)
        self.le_selected_file.setObjectName(u"le_selected_file")
        self.le_selected_file.setEnabled(True)
        self.le_selected_file.setReadOnly(True)

        self.layout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.le_selected_file)

        self.pb_analyse = QPushButton(self.tab_file_selection)
        self.pb_analyse.setObjectName(u"pb_analyse")

        self.layout.setWidget(6, QFormLayout.ItemRole.SpanningRole, self.pb_analyse)

        self.label_root = QLabel(self.tab_file_selection)
        self.label_root.setObjectName(u"label_root")
        self.label_root.setFrameShape(QFrame.Shape.StyledPanel)
        self.label_root.setFrameShadow(QFrame.Shadow.Raised)
        self.label_root.setScaledContents(True)
        self.label_root.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_root.setWordWrap(True)

        self.layout.setWidget(2, QFormLayout.ItemRole.SpanningRole, self.label_root)

        self.tabWidget.addTab(self.tab_file_selection, "")
        self.tab_parameters = QWidget()
        self.tab_parameters.setObjectName(u"tab_parameters")
        self.layout_AnalyserParameters = QGridLayout(self.tab_parameters)
        self.layout_AnalyserParameters.setObjectName(u"layout_AnalyserParameters")
        self.layout_AnalyserParameters.setContentsMargins(6, 6, 6, 6)
        self.ParameterTreeViewPlaceholder = QWidget(self.tab_parameters)
        self.ParameterTreeViewPlaceholder.setObjectName(u"ParameterTreeViewPlaceholder")

        self.layout_AnalyserParameters.addWidget(self.ParameterTreeViewPlaceholder, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tab_parameters, "")

        self.verticalLayout.addWidget(self.tabWidget)


        self.retranslateUi(AnalyserControlsWidget)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(AnalyserControlsWidget)
    # setupUi

    def retranslateUi(self, AnalyserControlsWidget):
        AnalyserControlsWidget.setWindowTitle(QCoreApplication.translate("AnalyserControlsWidget", u"AnalyserControlsWidget", None))
        self.label_selected.setText(QCoreApplication.translate("AnalyserControlsWidget", u"Selected File:", None))
        self.pb_root_directory.setText(QCoreApplication.translate("AnalyserControlsWidget", u"Change Root Directory", None))
        self.pb_analyse.setText(QCoreApplication.translate("AnalyserControlsWidget", u"Analyse", None))
        self.label_root.setText(QCoreApplication.translate("AnalyserControlsWidget", u"Root: ", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_file_selection), QCoreApplication.translate("AnalyserControlsWidget", u"File Selection", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_parameters), QCoreApplication.translate("AnalyserControlsWidget", u"Parameters", None))
    # retranslateUi


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './displot_image.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ImageTabPrototype(object):
    def setupUi(self, ImageTabPrototype):
        ImageTabPrototype.setObjectName("ImageTabPrototype")
        ImageTabPrototype.resize(1000, 700)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ImageTabPrototype.sizePolicy().hasHeightForWidth())
        ImageTabPrototype.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(ImageTabPrototype)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(ImageTabPrototype)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.splitter.setFrameShadow(QtWidgets.QFrame.Plain)
        self.splitter.setLineWidth(1)
        self.splitter.setMidLineWidth(3)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setOpaqueResize(True)
        self.splitter.setHandleWidth(6)
        self.splitter.setObjectName("splitter")
        self.imageView = WorkImageView(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageView.sizePolicy().hasHeightForWidth())
        self.imageView.setSizePolicy(sizePolicy)
        self.imageView.setMinimumSize(QtCore.QSize(400, 400))
        self.imageView.setObjectName("imageView")
        self.sidebar = QtWidgets.QWidget(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sidebar.sizePolicy().hasHeightForWidth())
        self.sidebar.setSizePolicy(sizePolicy)
        self.sidebar.setMinimumSize(QtCore.QSize(300, 0))
        self.sidebar.setMaximumSize(QtCore.QSize(300, 16777215))
        self.sidebar.setObjectName("sidebar")
        self.sidebarLayout = QtWidgets.QVBoxLayout(self.sidebar)
        self.sidebarLayout.setContentsMargins(3, 0, 0, 0)
        self.sidebarLayout.setObjectName("sidebarLayout")
        self.toolBox = QtWidgets.QTabWidget(self.sidebar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy)
        self.toolBox.setTabPosition(QtWidgets.QTabWidget.West)
        self.toolBox.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.toolBox.setUsesScrollButtons(True)
        self.toolBox.setTabBarAutoHide(False)
        self.toolBox.setObjectName("toolBox")
        self.imageTools = QtWidgets.QWidget()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageTools.sizePolicy().hasHeightForWidth())
        self.imageTools.setSizePolicy(sizePolicy)
        self.imageTools.setObjectName("imageTools")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.imageTools)
        self.verticalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.button_Scan = QtWidgets.QPushButton(self.imageTools)
        self.button_Scan.setFlat(False)
        self.button_Scan.setObjectName("button_Scan")
        self.verticalLayout_2.addWidget(self.button_Scan)
        self.imageToolsScroll = QtWidgets.QScrollArea(self.imageTools)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageToolsScroll.sizePolicy().hasHeightForWidth())
        self.imageToolsScroll.setSizePolicy(sizePolicy)
        self.imageToolsScroll.setFrameShape(QtWidgets.QFrame.Box)
        self.imageToolsScroll.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.imageToolsScroll.setLineWidth(1)
        self.imageToolsScroll.setMidLineWidth(0)
        self.imageToolsScroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.imageToolsScroll.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.imageToolsScroll.setWidgetResizable(True)
        self.imageToolsScroll.setObjectName("imageToolsScroll")
        self.imageToolsScrollArea = QtWidgets.QWidget()
        self.imageToolsScrollArea.setGeometry(QtCore.QRect(0, 0, 256, 322))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageToolsScrollArea.sizePolicy().hasHeightForWidth())
        self.imageToolsScrollArea.setSizePolicy(sizePolicy)
        self.imageToolsScrollArea.setObjectName("imageToolsScrollArea")
        self.formLayout_2 = QtWidgets.QFormLayout(self.imageToolsScrollArea)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_step1 = QtWidgets.QLabel(self.imageToolsScrollArea)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_step1.sizePolicy().hasHeightForWidth())
        self.label_step1.setSizePolicy(sizePolicy)
        self.label_step1.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_step1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_step1.setObjectName("label_step1")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.label_step1)
        self.label_MinFeatureArea = QtWidgets.QLabel(self.imageToolsScrollArea)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_MinFeatureArea.sizePolicy().hasHeightForWidth())
        self.label_MinFeatureArea.setSizePolicy(sizePolicy)
        self.label_MinFeatureArea.setWordWrap(True)
        self.label_MinFeatureArea.setObjectName("label_MinFeatureArea")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_MinFeatureArea)
        self.value_MinFeatureArea = QtWidgets.QSpinBox(self.imageToolsScrollArea)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.value_MinFeatureArea.sizePolicy().hasHeightForWidth())
        self.value_MinFeatureArea.setSizePolicy(sizePolicy)
        self.value_MinFeatureArea.setMinimumSize(QtCore.QSize(75, 0))
        self.value_MinFeatureArea.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.value_MinFeatureArea.setMaximum(1000)
        self.value_MinFeatureArea.setProperty("value", 15)
        self.value_MinFeatureArea.setDisplayIntegerBase(10)
        self.value_MinFeatureArea.setObjectName("value_MinFeatureArea")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.value_MinFeatureArea)
        self.label_MaxBboxOverlap = QtWidgets.QLabel(self.imageToolsScrollArea)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_MaxBboxOverlap.sizePolicy().hasHeightForWidth())
        self.label_MaxBboxOverlap.setSizePolicy(sizePolicy)
        self.label_MaxBboxOverlap.setWordWrap(True)
        self.label_MaxBboxOverlap.setObjectName("label_MaxBboxOverlap")
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.label_MaxBboxOverlap)
        self.value_MaxBboxOverlap = QtWidgets.QSpinBox(self.imageToolsScrollArea)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.value_MaxBboxOverlap.sizePolicy().hasHeightForWidth())
        self.value_MaxBboxOverlap.setSizePolicy(sizePolicy)
        self.value_MaxBboxOverlap.setMinimumSize(QtCore.QSize(75, 0))
        self.value_MaxBboxOverlap.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.value_MaxBboxOverlap.setMaximum(100)
        self.value_MaxBboxOverlap.setProperty("value", 33)
        self.value_MaxBboxOverlap.setObjectName("value_MaxBboxOverlap")
        self.formLayout_2.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.value_MaxBboxOverlap)
        self.label_step2 = QtWidgets.QLabel(self.imageToolsScrollArea)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_step2.sizePolicy().hasHeightForWidth())
        self.label_step2.setSizePolicy(sizePolicy)
        self.label_step2.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_step2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_step2.setObjectName("label_step2")
        self.formLayout_2.setWidget(6, QtWidgets.QFormLayout.SpanningRole, self.label_step2)
        self.label_CannySigma = QtWidgets.QLabel(self.imageToolsScrollArea)
        self.label_CannySigma.setWordWrap(True)
        self.label_CannySigma.setObjectName("label_CannySigma")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_CannySigma)
        self.value_CannySigma = QtWidgets.QDoubleSpinBox(self.imageToolsScrollArea)
        self.value_CannySigma.setMaximum(100.0)
        self.value_CannySigma.setSingleStep(0.1)
        self.value_CannySigma.setProperty("value", 0.33)
        self.value_CannySigma.setObjectName("value_CannySigma")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.value_CannySigma)
        self.label_MaxOverlap = QtWidgets.QLabel(self.imageToolsScrollArea)
        self.label_MaxOverlap.setWordWrap(True)
        self.label_MaxOverlap.setObjectName("label_MaxOverlap")
        self.formLayout_2.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.label_MaxOverlap)
        self.value_MaxOverlap = QtWidgets.QSpinBox(self.imageToolsScrollArea)
        self.value_MaxOverlap.setMaximum(100)
        self.value_MaxOverlap.setProperty("value", 75)
        self.value_MaxOverlap.setObjectName("value_MaxOverlap")
        self.formLayout_2.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.value_MaxOverlap)
        self.label_DetailSkew = QtWidgets.QLabel(self.imageToolsScrollArea)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_DetailSkew.sizePolicy().hasHeightForWidth())
        self.label_DetailSkew.setSizePolicy(sizePolicy)
        self.label_DetailSkew.setWordWrap(True)
        self.label_DetailSkew.setObjectName("label_DetailSkew")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_DetailSkew)
        self.value_DetailSkew = QtWidgets.QDoubleSpinBox(self.imageToolsScrollArea)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.value_DetailSkew.sizePolicy().hasHeightForWidth())
        self.value_DetailSkew.setSizePolicy(sizePolicy)
        self.value_DetailSkew.setMinimumSize(QtCore.QSize(75, 0))
        self.value_DetailSkew.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.value_DetailSkew.setFrame(True)
        self.value_DetailSkew.setPrefix("")
        self.value_DetailSkew.setDecimals(1)
        self.value_DetailSkew.setMaximum(100.0)
        self.value_DetailSkew.setSingleStep(0.1)
        self.value_DetailSkew.setProperty("value", 75.0)
        self.value_DetailSkew.setObjectName("value_DetailSkew")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.value_DetailSkew)
        self.label_FGMedian = QtWidgets.QLabel(self.imageToolsScrollArea)
        self.label_FGMedian.setObjectName("label_FGMedian")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_FGMedian)
        self.label_BGMedian = QtWidgets.QLabel(self.imageToolsScrollArea)
        self.label_BGMedian.setObjectName("label_BGMedian")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_BGMedian)
        self.value_FGMedian = QtWidgets.QSpinBox(self.imageToolsScrollArea)
        self.value_FGMedian.setMinimum(1)
        self.value_FGMedian.setSingleStep(2)
        self.value_FGMedian.setProperty("value", 3)
        self.value_FGMedian.setObjectName("value_FGMedian")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.value_FGMedian)
        self.value_BGMedian = QtWidgets.QSpinBox(self.imageToolsScrollArea)
        self.value_BGMedian.setMinimum(1)
        self.value_BGMedian.setSingleStep(2)
        self.value_BGMedian.setProperty("value", 21)
        self.value_BGMedian.setObjectName("value_BGMedian")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.value_BGMedian)
        self.imageToolsScroll.setWidget(self.imageToolsScrollArea)
        self.verticalLayout_2.addWidget(self.imageToolsScroll)
        self.toolBox.addTab(self.imageTools, "")
        self.labelledItems = QtWidgets.QWidget()
        self.labelledItems.setObjectName("labelledItems")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.labelledItems)
        self.verticalLayout_3.setContentsMargins(3, 3, 3, 3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.fragmentList = ImageTabList(self.labelledItems)
        self.fragmentList.setFrameShape(QtWidgets.QFrame.Box)
        self.fragmentList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.fragmentList.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.fragmentList.setAutoScroll(True)
        self.fragmentList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.fragmentList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.fragmentList.setSortingEnabled(True)
        self.fragmentList.setObjectName("fragmentList")
        self.fragmentList.horizontalHeader().setDefaultSectionSize(70)
        self.fragmentList.horizontalHeader().setHighlightSections(False)
        self.fragmentList.horizontalHeader().setMinimumSectionSize(20)
        self.fragmentList.horizontalHeader().setStretchLastSection(False)
        self.fragmentList.verticalHeader().setVisible(False)
        self.fragmentList.verticalHeader().setCascadingSectionResizes(False)
        self.fragmentList.verticalHeader().setDefaultSectionSize(1)
        self.fragmentList.verticalHeader().setMinimumSectionSize(20)
        self.fragmentList.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_3.addWidget(self.fragmentList)
        self.dislocationTools = QtWidgets.QWidget(self.labelledItems)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dislocationTools.sizePolicy().hasHeightForWidth())
        self.dislocationTools.setSizePolicy(sizePolicy)
        self.dislocationTools.setObjectName("dislocationTools")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.dislocationTools)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_HideAllFrags = QtWidgets.QPushButton(self.dislocationTools)
        self.button_HideAllFrags.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/feathericons/vendor/feather/icons/eye-off.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_HideAllFrags.setIcon(icon)
        self.button_HideAllFrags.setCheckable(True)
        self.button_HideAllFrags.setChecked(False)
        self.button_HideAllFrags.setObjectName("button_HideAllFrags")
        self.horizontalLayout_2.addWidget(self.button_HideAllFrags)
        self.button_AutoCenterFrags = QtWidgets.QPushButton(self.dislocationTools)
        self.button_AutoCenterFrags.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/feathericons/vendor/feather/icons/map-pin.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_AutoCenterFrags.setIcon(icon1)
        self.button_AutoCenterFrags.setCheckable(True)
        self.button_AutoCenterFrags.setChecked(True)
        self.button_AutoCenterFrags.setObjectName("button_AutoCenterFrags")
        self.horizontalLayout_2.addWidget(self.button_AutoCenterFrags)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.button_AddFrag = QtWidgets.QPushButton(self.dislocationTools)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_AddFrag.sizePolicy().hasHeightForWidth())
        self.button_AddFrag.setSizePolicy(sizePolicy)
        self.button_AddFrag.setMaximumSize(QtCore.QSize(50, 16777215))
        self.button_AddFrag.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/feathericons/vendor/feather/icons/plus-square.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_AddFrag.setIcon(icon2)
        self.button_AddFrag.setObjectName("button_AddFrag")
        self.horizontalLayout_2.addWidget(self.button_AddFrag)
        self.button_RemFrag = QtWidgets.QPushButton(self.dislocationTools)
        self.button_RemFrag.setMaximumSize(QtCore.QSize(50, 16777215))
        self.button_RemFrag.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/feathericons/vendor/feather/icons/minus-square.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_RemFrag.setIcon(icon3)
        self.button_RemFrag.setObjectName("button_RemFrag")
        self.horizontalLayout_2.addWidget(self.button_RemFrag)
        self.button_MovFrag = QtWidgets.QPushButton(self.dislocationTools)
        self.button_MovFrag.setMaximumSize(QtCore.QSize(50, 16777215))
        self.button_MovFrag.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/feathericons/vendor/feather/icons/move.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.button_MovFrag.setIcon(icon4)
        self.button_MovFrag.setObjectName("button_MovFrag")
        self.horizontalLayout_2.addWidget(self.button_MovFrag)
        self.verticalLayout_3.addWidget(self.dislocationTools)
        self.toolBox.addTab(self.labelledItems, "")
        self.sidebarLayout.addWidget(self.toolBox)
        self.minimap = MinimapView(self.sidebar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.minimap.sizePolicy().hasHeightForWidth())
        self.minimap.setSizePolicy(sizePolicy)
        self.minimap.setMinimumSize(QtCore.QSize(150, 200))
        self.minimap.setMaximumSize(QtCore.QSize(300, 200))
        self.minimap.setBaseSize(QtCore.QSize(0, 0))
        self.minimap.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.minimap.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.minimap.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.minimap.setObjectName("minimap")
        self.sidebarLayout.addWidget(self.minimap)
        self.verticalLayout.addWidget(self.splitter)
        self.imageInfo = QtWidgets.QWidget(ImageTabPrototype)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageInfo.sizePolicy().hasHeightForWidth())
        self.imageInfo.setSizePolicy(sizePolicy)
        self.imageInfo.setObjectName("imageInfo")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.imageInfo)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.imageInfoLabel = QtWidgets.QLabel(self.imageInfo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageInfoLabel.sizePolicy().hasHeightForWidth())
        self.imageInfoLabel.setSizePolicy(sizePolicy)
        self.imageInfoLabel.setMinimumSize(QtCore.QSize(300, 0))
        self.imageInfoLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.imageInfoLabel.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.imageInfoLabel.setObjectName("imageInfoLabel")
        self.horizontalLayout.addWidget(self.imageInfoLabel)
        self.imageCurX = QtWidgets.QLabel(self.imageInfo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageCurX.sizePolicy().hasHeightForWidth())
        self.imageCurX.setSizePolicy(sizePolicy)
        self.imageCurX.setMinimumSize(QtCore.QSize(60, 0))
        self.imageCurX.setFrameShape(QtWidgets.QFrame.Box)
        self.imageCurX.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.imageCurX.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.imageCurX.setObjectName("imageCurX")
        self.horizontalLayout.addWidget(self.imageCurX)
        self.imageCurY = QtWidgets.QLabel(self.imageInfo)
        self.imageCurY.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageCurY.sizePolicy().hasHeightForWidth())
        self.imageCurY.setSizePolicy(sizePolicy)
        self.imageCurY.setMinimumSize(QtCore.QSize(60, 0))
        self.imageCurY.setFrameShape(QtWidgets.QFrame.Box)
        self.imageCurY.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.imageCurY.setObjectName("imageCurY")
        self.horizontalLayout.addWidget(self.imageCurY)
        self.imageZoom = QtWidgets.QFrame(self.imageInfo)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageZoom.sizePolicy().hasHeightForWidth())
        self.imageZoom.setSizePolicy(sizePolicy)
        self.imageZoom.setMinimumSize(QtCore.QSize(100, 0))
        self.imageZoom.setMaximumSize(QtCore.QSize(120, 16777215))
        self.imageZoom.setFrameShape(QtWidgets.QFrame.Box)
        self.imageZoom.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.imageZoom.setObjectName("imageZoom")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.imageZoom)
        self.horizontalLayout_3.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout_3.setSpacing(1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_zoom = QtWidgets.QLabel(self.imageZoom)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_zoom.sizePolicy().hasHeightForWidth())
        self.label_zoom.setSizePolicy(sizePolicy)
        self.label_zoom.setMinimumSize(QtCore.QSize(100, 0))
        self.label_zoom.setOpenExternalLinks(False)
        self.label_zoom.setObjectName("label_zoom")
        self.horizontalLayout_3.addWidget(self.label_zoom)
        self.zoomDial = QtWidgets.QSpinBox(self.imageZoom)
        self.zoomDial.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.zoomDial.setFont(font)
        self.zoomDial.setMinimum(10)
        self.zoomDial.setMaximum(400)
        self.zoomDial.setProperty("value", 100)
        self.zoomDial.setObjectName("zoomDial")
        self.horizontalLayout_3.addWidget(self.zoomDial)
        self.horizontalLayout.addWidget(self.imageZoom)
        self.verticalLayout.addWidget(self.imageInfo)
        self.label_MinFeatureArea.setBuddy(self.value_MinFeatureArea)
        self.label_MaxBboxOverlap.setBuddy(self.value_MaxBboxOverlap)
        self.label_CannySigma.setBuddy(self.value_CannySigma)
        self.label_MaxOverlap.setBuddy(self.value_MaxOverlap)
        self.label_DetailSkew.setBuddy(self.value_DetailSkew)
        self.label_FGMedian.setBuddy(self.value_FGMedian)
        self.label_BGMedian.setBuddy(self.value_BGMedian)

        self.retranslateUi(ImageTabPrototype)
        self.toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ImageTabPrototype)

    def retranslateUi(self, ImageTabPrototype):
        _translate = QtCore.QCoreApplication.translate
        ImageTabPrototype.setWindowTitle(_translate("ImageTabPrototype", "Form"))
        self.button_Scan.setText(_translate("ImageTabPrototype", "Scan image"))
        self.label_step1.setText(_translate("ImageTabPrototype", "<html><head/><body><p><span style=\" font-weight:600;\">Step 1:</span> Feature selection</p></body></html>"))
        self.label_MinFeatureArea.setText(_translate("ImageTabPrototype", "Minimum feature area"))
        self.value_MinFeatureArea.setSuffix(_translate("ImageTabPrototype", "px"))
        self.label_MaxBboxOverlap.setText(_translate("ImageTabPrototype", "Maximum bounding box overlap"))
        self.value_MaxBboxOverlap.setSuffix(_translate("ImageTabPrototype", "%"))
        self.label_step2.setText(_translate("ImageTabPrototype", "<html><head/><body><p><span style=\" font-weight:600;\">Step 2:</span> Discrimination</p></body></html>"))
        self.label_CannySigma.setText(_translate("ImageTabPrototype", "<html><head/><body><p>Canny threshold sigma<br/><span style=\" font-style:italic;\">(increase for more edges)</span></p></body></html>"))
        self.label_MaxOverlap.setText(_translate("ImageTabPrototype", "Maximum pixelwise overlap"))
        self.value_MaxOverlap.setSuffix(_translate("ImageTabPrototype", "%"))
        self.label_DetailSkew.setText(_translate("ImageTabPrototype", "<html><head/><body><p>Detail level skew<br/><span style=\" font-style:italic;\">(larger % = less small details)</span></p></body></html>"))
        self.value_DetailSkew.setSuffix(_translate("ImageTabPrototype", "%"))
        self.label_FGMedian.setText(_translate("ImageTabPrototype", "Foreground median blur"))
        self.label_BGMedian.setText(_translate("ImageTabPrototype", "Background median blur"))
        self.toolBox.setTabText(self.toolBox.indexOf(self.imageTools), _translate("ImageTabPrototype", "Detection"))
        self.button_HideAllFrags.setToolTip(_translate("ImageTabPrototype", "Toggle this button to show/hide all fragments."))
        self.button_AutoCenterFrags.setToolTip(_translate("ImageTabPrototype", "Toggle this button to control whether the view will\n"
"automatically center on fragments selected on the list."))
        self.button_AddFrag.setToolTip(_translate("ImageTabPrototype", "Add new fragment to image."))
        self.button_RemFrag.setToolTip(_translate("ImageTabPrototype", "Remove selected fragments from image.\n"
"Selection is controlled using the checkboxes in the table above."))
        self.button_MovFrag.setToolTip(_translate("ImageTabPrototype", "Move selected fragment.\n"
"Selection is controlled by highlighting a row in the table above."))
        self.toolBox.setTabText(self.toolBox.indexOf(self.labelledItems), _translate("ImageTabPrototype", "Fragments"))
        self.imageInfoLabel.setText(_translate("ImageTabPrototype", "No image loaded"))
        self.imageCurX.setText(_translate("ImageTabPrototype", "x:0"))
        self.imageCurY.setText(_translate("ImageTabPrototype", "y:0"))
        self.label_zoom.setText(_translate("ImageTabPrototype", "Zoom:"))
        self.zoomDial.setSuffix(_translate("ImageTabPrototype", "%"))

from displot.ui_widgets import ImageTabList, MinimapView, WorkImageView
from . import feathericons_rc

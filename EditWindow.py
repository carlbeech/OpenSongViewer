# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EditWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1542, 900)
        Dialog.setMinimumSize(QtCore.QSize(500, 500))
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QtWidgets.QFrame(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 22))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setMidLineWidth(-1)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_10 = QtWidgets.QFrame(self.frame_2)
        self.frame_10.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_10)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label = QtWidgets.QLabel(self.frame_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(150, 0))
        self.label.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout_4.addWidget(self.label, 0, 0, 1, 1)
        self.FName = QtWidgets.QLineEdit(self.frame_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FName.sizePolicy().hasHeightForWidth())
        self.FName.setSizePolicy(sizePolicy)
        self.FName.setMinimumSize(QtCore.QSize(200, 20))
        self.FName.setMaximumSize(QtCore.QSize(400, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.FName.setFont(font)
        self.FName.setObjectName("FName")
        self.gridLayout_4.addWidget(self.FName, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.frame_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(130, 0))
        self.label_4.setMaximumSize(QtCore.QSize(130, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout_4.addWidget(self.label_4, 1, 0, 1, 1)
        self.SongKey = QtWidgets.QComboBox(self.frame_10)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SongKey.sizePolicy().hasHeightForWidth())
        self.SongKey.setSizePolicy(sizePolicy)
        self.SongKey.setMinimumSize(QtCore.QSize(100, 0))
        self.SongKey.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.SongKey.setFont(font)
        self.SongKey.setObjectName("SongKey")
        self.SongKey.addItem("")
        self.SongKey.addItem("")
        self.SongKey.addItem("")
        self.SongKey.addItem("")
        self.SongKey.addItem("")
        self.SongKey.addItem("")
        self.SongKey.addItem("")
        self.SongKey.addItem("")
        self.SongKey.addItem("")
        self.SongKey.addItem("")
        self.SongKey.addItem("")
        self.SongKey.addItem("")
        self.gridLayout_4.addWidget(self.SongKey, 1, 1, 1, 1)
        self.horizontalLayout.addWidget(self.frame_10)
        self.frame_4 = QtWidgets.QFrame(self.frame_2)
        self.frame_4.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_4.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_6 = QtWidgets.QFrame(self.frame_4)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(200, 0))
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_2.addWidget(self.frame_6)
        self.frame_7 = QtWidgets.QFrame(self.frame_4)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_7)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.PageSize = QtWidgets.QComboBox(self.frame_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PageSize.sizePolicy().hasHeightForWidth())
        self.PageSize.setSizePolicy(sizePolicy)
        self.PageSize.setMinimumSize(QtCore.QSize(150, 30))
        self.PageSize.setMaximumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.PageSize.setFont(font)
        self.PageSize.setObjectName("PageSize")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.PageSize.addItem("")
        self.gridLayout_3.addWidget(self.PageSize, 1, 1, 1, 1)
        self.PageSize_Portrait = QtWidgets.QComboBox(self.frame_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PageSize_Portrait.sizePolicy().hasHeightForWidth())
        self.PageSize_Portrait.setSizePolicy(sizePolicy)
        self.PageSize_Portrait.setMinimumSize(QtCore.QSize(150, 30))
        self.PageSize_Portrait.setMaximumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.PageSize_Portrait.setFont(font)
        self.PageSize_Portrait.setObjectName("PageSize_Portrait")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.PageSize_Portrait.addItem("")
        self.gridLayout_3.addWidget(self.PageSize_Portrait, 1, 3, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.frame_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setMinimumSize(QtCore.QSize(120, 0))
        self.label_10.setMaximumSize(QtCore.QSize(120, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_10.setWordWrap(True)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 1, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.frame_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_9.sizePolicy().hasHeightForWidth())
        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QtCore.QSize(140, 0))
        self.label_9.setMaximumSize(QtCore.QSize(140, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_9.setWordWrap(True)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 1, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.frame_7)
        self.horizontalLayout.addWidget(self.frame_4)
        self.frame_5 = QtWidgets.QFrame(self.frame_2)
        self.frame_5.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.frame_8 = QtWidgets.QFrame(self.frame_5)
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(150, 0))
        self.label_2.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        spacerItem1 = QtWidgets.QSpacerItem(416, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.verticalLayout_3.addWidget(self.frame_8)
        self.frame_9 = QtWidgets.QFrame(self.frame_5)
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_9)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_7 = QtWidgets.QLabel(self.frame_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QtCore.QSize(140, 0))
        self.label_7.setMaximumSize(QtCore.QSize(140, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_7.setWordWrap(True)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 1, 0, 1, 1)
        self.DefaultFontSize = QtWidgets.QComboBox(self.frame_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DefaultFontSize.sizePolicy().hasHeightForWidth())
        self.DefaultFontSize.setSizePolicy(sizePolicy)
        self.DefaultFontSize.setMinimumSize(QtCore.QSize(150, 30))
        self.DefaultFontSize.setMaximumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.DefaultFontSize.setFont(font)
        self.DefaultFontSize.setObjectName("DefaultFontSize")
        self.DefaultFontSize.addItem("")
        self.DefaultFontSize.addItem("")
        self.DefaultFontSize.addItem("")
        self.DefaultFontSize.addItem("")
        self.DefaultFontSize.addItem("")
        self.DefaultFontSize.addItem("")
        self.DefaultFontSize.addItem("")
        self.DefaultFontSize.addItem("")
        self.DefaultFontSize.addItem("")
        self.DefaultFontSize.addItem("")
        self.DefaultFontSize.addItem("")
        self.DefaultFontSize.addItem("")
        self.DefaultFontSize.addItem("")
        self.DefaultFontSize.addItem("")
        self.DefaultFontSize.addItem("")
        self.DefaultFontSize.addItem("")
        self.DefaultFontSize.addItem("")
        self.DefaultFontSize.addItem("")
        self.DefaultFontSize.addItem("")
        self.gridLayout_2.addWidget(self.DefaultFontSize, 1, 1, 1, 1)
        self.DefaultFontSize_Portrait = QtWidgets.QComboBox(self.frame_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DefaultFontSize_Portrait.sizePolicy().hasHeightForWidth())
        self.DefaultFontSize_Portrait.setSizePolicy(sizePolicy)
        self.DefaultFontSize_Portrait.setMinimumSize(QtCore.QSize(150, 30))
        self.DefaultFontSize_Portrait.setMaximumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.DefaultFontSize_Portrait.setFont(font)
        self.DefaultFontSize_Portrait.setObjectName("DefaultFontSize_Portrait")
        self.DefaultFontSize_Portrait.addItem("")
        self.DefaultFontSize_Portrait.addItem("")
        self.DefaultFontSize_Portrait.addItem("")
        self.DefaultFontSize_Portrait.addItem("")
        self.DefaultFontSize_Portrait.addItem("")
        self.DefaultFontSize_Portrait.addItem("")
        self.DefaultFontSize_Portrait.addItem("")
        self.DefaultFontSize_Portrait.addItem("")
        self.DefaultFontSize_Portrait.addItem("")
        self.DefaultFontSize_Portrait.addItem("")
        self.DefaultFontSize_Portrait.addItem("")
        self.DefaultFontSize_Portrait.addItem("")
        self.DefaultFontSize_Portrait.addItem("")
        self.DefaultFontSize_Portrait.addItem("")
        self.DefaultFontSize_Portrait.addItem("")
        self.DefaultFontSize_Portrait.addItem("")
        self.DefaultFontSize_Portrait.addItem("")
        self.DefaultFontSize_Portrait.addItem("")
        self.DefaultFontSize_Portrait.addItem("")
        self.gridLayout_2.addWidget(self.DefaultFontSize_Portrait, 1, 3, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.frame_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QtCore.QSize(120, 0))
        self.label_8.setMaximumSize(QtCore.QSize(120, 16777215))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_8.setWordWrap(True)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 1, 2, 1, 1)
        self.verticalLayout_3.addWidget(self.frame_9)
        self.horizontalLayout.addWidget(self.frame_5)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.EditingSongText = QtWidgets.QPlainTextEdit(self.frame_3)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        self.EditingSongText.setFont(font)
        self.EditingSongText.setObjectName("EditingSongText")
        self.horizontalLayout_2.addWidget(self.EditingSongText)
        self.verticalLayout.addWidget(self.frame_3)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "File Name:"))
        self.label_4.setText(_translate("Dialog", "Base Key:"))
        self.SongKey.setItemText(0, _translate("Dialog", "C"))
        self.SongKey.setItemText(1, _translate("Dialog", "Db"))
        self.SongKey.setItemText(2, _translate("Dialog", "D"))
        self.SongKey.setItemText(3, _translate("Dialog", "Eb"))
        self.SongKey.setItemText(4, _translate("Dialog", "E"))
        self.SongKey.setItemText(5, _translate("Dialog", "F"))
        self.SongKey.setItemText(6, _translate("Dialog", "Gb"))
        self.SongKey.setItemText(7, _translate("Dialog", "G"))
        self.SongKey.setItemText(8, _translate("Dialog", "Ab"))
        self.SongKey.setItemText(9, _translate("Dialog", "A"))
        self.SongKey.setItemText(10, _translate("Dialog", "Bb"))
        self.SongKey.setItemText(11, _translate("Dialog", "B"))
        self.label_3.setText(_translate("Dialog", "Lines Before Split:"))
        self.PageSize.setItemText(0, _translate("Dialog", "Default"))
        self.PageSize.setItemText(1, _translate("Dialog", "20"))
        self.PageSize.setItemText(2, _translate("Dialog", "21"))
        self.PageSize.setItemText(3, _translate("Dialog", "22"))
        self.PageSize.setItemText(4, _translate("Dialog", "23"))
        self.PageSize.setItemText(5, _translate("Dialog", "24"))
        self.PageSize.setItemText(6, _translate("Dialog", "25"))
        self.PageSize.setItemText(7, _translate("Dialog", "26"))
        self.PageSize.setItemText(8, _translate("Dialog", "27"))
        self.PageSize.setItemText(9, _translate("Dialog", "28"))
        self.PageSize.setItemText(10, _translate("Dialog", "29"))
        self.PageSize.setItemText(11, _translate("Dialog", "30"))
        self.PageSize.setItemText(12, _translate("Dialog", "31"))
        self.PageSize.setItemText(13, _translate("Dialog", "32"))
        self.PageSize.setItemText(14, _translate("Dialog", "33"))
        self.PageSize.setItemText(15, _translate("Dialog", "34"))
        self.PageSize.setItemText(16, _translate("Dialog", "35"))
        self.PageSize.setItemText(17, _translate("Dialog", "36"))
        self.PageSize.setItemText(18, _translate("Dialog", "37"))
        self.PageSize.setItemText(19, _translate("Dialog", "38"))
        self.PageSize.setItemText(20, _translate("Dialog", "39"))
        self.PageSize.setItemText(21, _translate("Dialog", "40"))
        self.PageSize.setItemText(22, _translate("Dialog", "41"))
        self.PageSize.setItemText(23, _translate("Dialog", "42"))
        self.PageSize.setItemText(24, _translate("Dialog", "43"))
        self.PageSize.setItemText(25, _translate("Dialog", "44"))
        self.PageSize.setItemText(26, _translate("Dialog", "45"))
        self.PageSize.setItemText(27, _translate("Dialog", "46"))
        self.PageSize.setItemText(28, _translate("Dialog", "47"))
        self.PageSize.setItemText(29, _translate("Dialog", "48"))
        self.PageSize.setItemText(30, _translate("Dialog", "49"))
        self.PageSize.setItemText(31, _translate("Dialog", "50"))
        self.PageSize_Portrait.setItemText(0, _translate("Dialog", "Default"))
        self.PageSize_Portrait.setItemText(1, _translate("Dialog", "20"))
        self.PageSize_Portrait.setItemText(2, _translate("Dialog", "21"))
        self.PageSize_Portrait.setItemText(3, _translate("Dialog", "22"))
        self.PageSize_Portrait.setItemText(4, _translate("Dialog", "23"))
        self.PageSize_Portrait.setItemText(5, _translate("Dialog", "24"))
        self.PageSize_Portrait.setItemText(6, _translate("Dialog", "25"))
        self.PageSize_Portrait.setItemText(7, _translate("Dialog", "26"))
        self.PageSize_Portrait.setItemText(8, _translate("Dialog", "27"))
        self.PageSize_Portrait.setItemText(9, _translate("Dialog", "28"))
        self.PageSize_Portrait.setItemText(10, _translate("Dialog", "29"))
        self.PageSize_Portrait.setItemText(11, _translate("Dialog", "30"))
        self.PageSize_Portrait.setItemText(12, _translate("Dialog", "31"))
        self.PageSize_Portrait.setItemText(13, _translate("Dialog", "32"))
        self.PageSize_Portrait.setItemText(14, _translate("Dialog", "33"))
        self.PageSize_Portrait.setItemText(15, _translate("Dialog", "34"))
        self.PageSize_Portrait.setItemText(16, _translate("Dialog", "35"))
        self.PageSize_Portrait.setItemText(17, _translate("Dialog", "36"))
        self.PageSize_Portrait.setItemText(18, _translate("Dialog", "37"))
        self.PageSize_Portrait.setItemText(19, _translate("Dialog", "38"))
        self.PageSize_Portrait.setItemText(20, _translate("Dialog", "39"))
        self.PageSize_Portrait.setItemText(21, _translate("Dialog", "40"))
        self.PageSize_Portrait.setItemText(22, _translate("Dialog", "41"))
        self.PageSize_Portrait.setItemText(23, _translate("Dialog", "42"))
        self.PageSize_Portrait.setItemText(24, _translate("Dialog", "43"))
        self.PageSize_Portrait.setItemText(25, _translate("Dialog", "44"))
        self.PageSize_Portrait.setItemText(26, _translate("Dialog", "45"))
        self.PageSize_Portrait.setItemText(27, _translate("Dialog", "46"))
        self.PageSize_Portrait.setItemText(28, _translate("Dialog", "47"))
        self.PageSize_Portrait.setItemText(29, _translate("Dialog", "48"))
        self.PageSize_Portrait.setItemText(30, _translate("Dialog", "49"))
        self.PageSize_Portrait.setItemText(31, _translate("Dialog", "50"))
        self.PageSize_Portrait.setItemText(32, _translate("Dialog", "51"))
        self.PageSize_Portrait.setItemText(33, _translate("Dialog", "52"))
        self.PageSize_Portrait.setItemText(34, _translate("Dialog", "53"))
        self.PageSize_Portrait.setItemText(35, _translate("Dialog", "54"))
        self.PageSize_Portrait.setItemText(36, _translate("Dialog", "55"))
        self.PageSize_Portrait.setItemText(37, _translate("Dialog", "56"))
        self.PageSize_Portrait.setItemText(38, _translate("Dialog", "57"))
        self.PageSize_Portrait.setItemText(39, _translate("Dialog", "58"))
        self.PageSize_Portrait.setItemText(40, _translate("Dialog", "59"))
        self.PageSize_Portrait.setItemText(41, _translate("Dialog", "60"))
        self.PageSize_Portrait.setItemText(42, _translate("Dialog", "61"))
        self.PageSize_Portrait.setItemText(43, _translate("Dialog", "62"))
        self.PageSize_Portrait.setItemText(44, _translate("Dialog", "63"))
        self.PageSize_Portrait.setItemText(45, _translate("Dialog", "64"))
        self.PageSize_Portrait.setItemText(46, _translate("Dialog", "65"))
        self.PageSize_Portrait.setItemText(47, _translate("Dialog", "66"))
        self.PageSize_Portrait.setItemText(48, _translate("Dialog", "67"))
        self.PageSize_Portrait.setItemText(49, _translate("Dialog", "68"))
        self.PageSize_Portrait.setItemText(50, _translate("Dialog", "69"))
        self.PageSize_Portrait.setItemText(51, _translate("Dialog", "70"))
        self.label_10.setText(_translate("Dialog", " Portrait:"))
        self.label_9.setText(_translate("Dialog", "Landscape:"))
        self.label_2.setText(_translate("Dialog", "Font Size:"))
        self.label_7.setText(_translate("Dialog", "Landscape:"))
        self.DefaultFontSize.setItemText(0, _translate("Dialog", "Default"))
        self.DefaultFontSize.setItemText(1, _translate("Dialog", "10"))
        self.DefaultFontSize.setItemText(2, _translate("Dialog", "15"))
        self.DefaultFontSize.setItemText(3, _translate("Dialog", "20"))
        self.DefaultFontSize.setItemText(4, _translate("Dialog", "22"))
        self.DefaultFontSize.setItemText(5, _translate("Dialog", "24"))
        self.DefaultFontSize.setItemText(6, _translate("Dialog", "26"))
        self.DefaultFontSize.setItemText(7, _translate("Dialog", "28"))
        self.DefaultFontSize.setItemText(8, _translate("Dialog", "30"))
        self.DefaultFontSize.setItemText(9, _translate("Dialog", "32"))
        self.DefaultFontSize.setItemText(10, _translate("Dialog", "34"))
        self.DefaultFontSize.setItemText(11, _translate("Dialog", "36"))
        self.DefaultFontSize.setItemText(12, _translate("Dialog", "38"))
        self.DefaultFontSize.setItemText(13, _translate("Dialog", "40"))
        self.DefaultFontSize.setItemText(14, _translate("Dialog", "42"))
        self.DefaultFontSize.setItemText(15, _translate("Dialog", "44"))
        self.DefaultFontSize.setItemText(16, _translate("Dialog", "46"))
        self.DefaultFontSize.setItemText(17, _translate("Dialog", "48"))
        self.DefaultFontSize.setItemText(18, _translate("Dialog", "50"))
        self.DefaultFontSize_Portrait.setItemText(0, _translate("Dialog", "Default"))
        self.DefaultFontSize_Portrait.setItemText(1, _translate("Dialog", "10"))
        self.DefaultFontSize_Portrait.setItemText(2, _translate("Dialog", "15"))
        self.DefaultFontSize_Portrait.setItemText(3, _translate("Dialog", "20"))
        self.DefaultFontSize_Portrait.setItemText(4, _translate("Dialog", "22"))
        self.DefaultFontSize_Portrait.setItemText(5, _translate("Dialog", "24"))
        self.DefaultFontSize_Portrait.setItemText(6, _translate("Dialog", "26"))
        self.DefaultFontSize_Portrait.setItemText(7, _translate("Dialog", "28"))
        self.DefaultFontSize_Portrait.setItemText(8, _translate("Dialog", "30"))
        self.DefaultFontSize_Portrait.setItemText(9, _translate("Dialog", "32"))
        self.DefaultFontSize_Portrait.setItemText(10, _translate("Dialog", "34"))
        self.DefaultFontSize_Portrait.setItemText(11, _translate("Dialog", "36"))
        self.DefaultFontSize_Portrait.setItemText(12, _translate("Dialog", "38"))
        self.DefaultFontSize_Portrait.setItemText(13, _translate("Dialog", "40"))
        self.DefaultFontSize_Portrait.setItemText(14, _translate("Dialog", "42"))
        self.DefaultFontSize_Portrait.setItemText(15, _translate("Dialog", "44"))
        self.DefaultFontSize_Portrait.setItemText(16, _translate("Dialog", "46"))
        self.DefaultFontSize_Portrait.setItemText(17, _translate("Dialog", "48"))
        self.DefaultFontSize_Portrait.setItemText(18, _translate("Dialog", "50"))
        self.label_8.setText(_translate("Dialog", " Portrait:"))

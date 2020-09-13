# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Prefs.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PrefsEditor(object):
    def setupUi(self, PrefsEditor):
        PrefsEditor.setObjectName("PrefsEditor")
        PrefsEditor.resize(600, 80)
        self.gridLayout_2 = QtWidgets.QGridLayout(PrefsEditor)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.frame = QtWidgets.QFrame(PrefsEditor)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.SongDirectory = QtWidgets.QLineEdit(self.frame)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.SongDirectory.setFont(font)
        self.SongDirectory.setObjectName("SongDirectory")
        self.gridLayout.addWidget(self.SongDirectory, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(PrefsEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(PrefsEditor)
        self.buttonBox.accepted.connect(PrefsEditor.accept)
        self.buttonBox.rejected.connect(PrefsEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(PrefsEditor)

    def retranslateUi(self, PrefsEditor):
        _translate = QtCore.QCoreApplication.translate
        PrefsEditor.setWindowTitle(_translate("PrefsEditor", "Dialog"))
        self.label.setText(_translate("PrefsEditor", "Directory of Songs:"))

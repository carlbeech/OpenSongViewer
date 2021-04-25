# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'About.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_About(object):
    def setupUi(self, About):
        About.setObjectName("About")
        About.resize(600, 400)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(About.sizePolicy().hasHeightForWidth())
        About.setSizePolicy(sizePolicy)
        About.setMinimumSize(QtCore.QSize(600, 400))
        self.gridLayout = QtWidgets.QGridLayout(About)
        self.gridLayout.setObjectName("gridLayout")
        self.aboutMessage = QtWidgets.QTextBrowser(About)
        self.aboutMessage.setMinimumSize(QtCore.QSize(550, 250))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.aboutMessage.setFont(font)
        self.aboutMessage.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.aboutMessage.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.aboutMessage.setFrameShadow(QtWidgets.QFrame.Plain)
        self.aboutMessage.setLineWidth(0)
        self.aboutMessage.setObjectName("aboutMessage")
        self.gridLayout.addWidget(self.aboutMessage, 0, 1, 2, 2)
        self.buttonBox = QtWidgets.QDialogButtonBox(About)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 4)

        self.retranslateUi(About)
        self.buttonBox.accepted.connect(About.accept)
        self.buttonBox.rejected.connect(About.reject)
        QtCore.QMetaObject.connectSlotsByName(About)

    def retranslateUi(self, About):
        _translate = QtCore.QCoreApplication.translate
        About.setWindowTitle(_translate("About", "Dialog"))

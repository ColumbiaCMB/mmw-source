# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'readout/mmw_source/gui/save_sweep.ui'
#
# Created: Fri Aug 29 12:37:40 2014
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SaveSweepPrompt(object):
    def setupUi(self, SaveSweepPrompt):
        SaveSweepPrompt.setObjectName(_fromUtf8("SaveSweepPrompt"))
        SaveSweepPrompt.resize(400, 300)
        self.verticalLayout = QtGui.QVBoxLayout(SaveSweepPrompt)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(SaveSweepPrompt)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.text_edit_comment = QtGui.QPlainTextEdit(SaveSweepPrompt)
        self.text_edit_comment.setObjectName(_fromUtf8("text_edit_comment"))
        self.verticalLayout.addWidget(self.text_edit_comment)
        self.buttonBox = QtGui.QDialogButtonBox(SaveSweepPrompt)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(SaveSweepPrompt)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SaveSweepPrompt.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SaveSweepPrompt.reject)
        QtCore.QMetaObject.connectSlotsByName(SaveSweepPrompt)

    def retranslateUi(self, SaveSweepPrompt):
        SaveSweepPrompt.setWindowTitle(QtGui.QApplication.translate("SaveSweepPrompt", "Save sweep", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SaveSweepPrompt", "Enter comment text to save with data file:", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    SaveSweepPrompt = QtGui.QDialog()
    ui = Ui_SaveSweepPrompt()
    ui.setupUi(SaveSweepPrompt)
    SaveSweepPrompt.show()
    sys.exit(app.exec_())


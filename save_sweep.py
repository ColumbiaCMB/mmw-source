import gui.save_sweep_ui
from PyQt4.QtGui import QDialog

class SaveSweepDialog(QDialog,gui.save_sweep_ui.Ui_SaveSweepPrompt):
    def __init__(self, parent=None):
        super(SaveSweepDialog, self).__init__(parent)
        self.setupUi(self)
    @staticmethod
    def promptToSave(parent = None):
        dialog = SaveSweepDialog(parent)
        result = dialog.exec_()
        comments = str(dialog.text_edit_comment.toPlainText())
        return comments,result


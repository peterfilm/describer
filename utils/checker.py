from PyQt5 import QtCore

class Checker(object):
    '''
    проверяем на включение-выключение
    '''
    def __init__(self, ui):
        self.ui = ui
    
    def check_photos(self):
        if self.ui.photos.photos:
            self.ui.comboBox_number.setEnabled(True)
            self.ui.lineEdit_add_describe.setEnabled(True)
            self.ui.comboBox_ai.setEnabled(True)
            self.ui.btn_add_to_text.setEnabled(True)
            self.ui.btn_ai_describe.setEnabled(True)
            self.ui.comboBox.setEnabled(True)
            self.ui.comboBox_begin.setEnabled(True)
            self.ui.comboBox_end.setEnabled(True)
            self.ui.comboBox_number.setEnabled(True)
            self.ui.btn_clear_all.setEnabled(True)
            self.ui.action_addPhotos.setEnabled(True)
            self.ui.action_saveList.setEnabled(True)
            self.ui.action_excel.setEnabled(True)
            self.ui.action_clearAll.setEnabled(True)
            self.ui.ai.combo_changed()
        else:
            self.ui.comboBox_number.setEnabled(False)
            self.ui.lineEdit_add_describe.setEnabled(False)
            self.ui.comboBox_ai.setEnabled(False)
            self.ui.btn_add_to_text.setEnabled(False)
            self.ui.btn_ai_describe.setEnabled(False)
            self.ui.comboBox.setEnabled(False)
            self.ui.comboBox_begin.setEnabled(False)
            self.ui.comboBox_end.setEnabled(False)
            self.ui.comboBox_number.setEnabled(False)
            self.ui.btn_clear_all.setEnabled(False)
            self.ui.action_addPhotos.setEnabled(False)
            self.ui.action_saveList.setEnabled(False)
            self.ui.action_excel.setEnabled(False)
            self.ui.action_clearAll.setEnabled(False)
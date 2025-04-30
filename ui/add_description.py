from PyQt5 import QtCore
import re

class AddDescription(object):
    '''
    Добавление описания в начало или в конец у всех фотографий
    '''
    def __init__(self, ui):
        self.ui = ui
        self.ui.lineEdit_add_describe.returnPressed.connect(self.add_text)
        self.ui.btn_add_to_text.clicked.connect(self.add_text)
        self.last_word = ''
        self.ui.comboBox_ai.model().item(2).setEnabled(False)
        
        # self.retranslateUi()
        self.ui.lang_changed.connect(self.retranslateUi)
        
    def check_change_btn(self):
        if self.last_word:
            self.ui.comboBox_ai.model().item(2).setEnabled(True)
        else:
            self.ui.comboBox_ai.model().item(2).setEnabled(False)    
            
    def retranslateUi(self):
        """Обновляем язык"""
        self.states = {
            "text_begin_updated": self.ui._translate("Describer", 'Текст успешно добавлен в начало'),
            "text_added_end": self.ui._translate("Describer", 'Текст успешно добавлен в конец'),
            "text_replaced": self.ui._translate("Describer", 'Текст успешно заменен'),
            "error": self.ui._translate("Describer", 'Что-то пошло не так...')
        }
              
    def add_text(self):
        if self.ui.lineEdit_add_describe.text():
            command = self.ui.comboBox_ai.currentText()
            if command == self.ui._translate('Describer', 'Добавить в начало'):
                for photo in self.ui.photos.photos:
                    text = self.ui.lineEdit_add_describe.text() + ' ' + photo.textEdit_photo.toPlainText()
                    photo.textEdit_photo.clear()
                    photo.textEdit_photo.insertPlainText(text)
                self.last_word = self.ui.lineEdit_add_describe.text()
                self.check_change_btn()
                self.ui.timer.on_clicked(self.states['text_begin_updated'], 5000)
                
            elif command == self.ui._translate('Describer', 'Добавить в конец'):
                for photo in self.ui.photos.photos:
                    photo.textEdit_photo.insertPlainText(' ' + self.ui.lineEdit_add_describe.text())
                self.last_word = self.ui.lineEdit_add_describe.text()
                self.check_change_btn()
                self.ui.timer.on_clicked(self.states['text_added_end'], 5000)
                
            elif command == self.ui._translate('Describer', 'Заменить'):
                if self.last_word:
                    try:
                        for photo in self.ui.photos.photos:
                                text = photo.textEdit_photo.toPlainText()
                                new_word = self.ui.lineEdit_add_describe.text()
                                new_text = re.sub(rf'{self.last_word}', new_word, text, flags = re.IGNORECASE)
                                photo.textEdit_photo.clear()
                                photo.textEdit_photo.insertPlainText(new_text)
                        self.last_word = new_word
                        self.check_change_btn()
                        self.ui.timer.on_clicked(self.states['text_replaced'], 5000)
                    except Exception as e:
                        self.ui.timer.on_clicked(self.states['error'], 5000)
                        print(e)
                        
                    
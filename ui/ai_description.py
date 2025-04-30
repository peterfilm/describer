import os
from PyQt5 import QtCore
from engine import Engine
from PyQt5.QtWidgets import QMessageBox

class AI_description(object):
    '''
    AI описание всех картинок
    '''
    
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.begin = self.ui.comboBox_begin.currentText()
        self.end = self.ui.comboBox_end.currentText()
        
        self.ui.comboBox_end.currentTextChanged.connect(self.end_change)
        
        self.ui.comboBox.currentTextChanged.connect(self.combo_changed)
        self.ui.btn_ai_describe.clicked.connect(self.run_ai)
        
        self.ui.btn_stop.clicked.connect(self.on_stop)
        
        self.ui.photos.photos_updated.connect(self.update_ranges)
        self.update_ranges()
        self.combo_changed()
        
        self.ui.btn_stop.setEnabled(False)
        
        self.ui.lang_changed.connect(self.retranslateUi)
        
    def retranslateUi(self):
        '''изменить язык'''
        self.translated_ai_number = self.ui._translate("Describer", "AI описание для фотографии №{index} - готово!")
        
        self.states = {
            "stopped_by_user": self.ui._translate("Describer", "Остановлено пользователем"),
            "ai_started": self.ui._translate("Describer", "AI описание для всех картинок запущено"),
            "error_title": self.ui._translate('Describer', 'Ошибка'),
            "error_message": self.ui._translate('Describer', 'Закончились токены на HuggingFace. Ждите следующий день'),
            
        }
        
        
    def run_ai(self):
        begin = int(self.ui.comboBox_begin.currentText()) - 1
        end = int(self.ui.comboBox_end.currentText())
        selector = True if self.ui.comboBox.currentText() == self.ui._translate('Describer', 'Все') else False
        
        if selector:
            paths = [i.path for i in self.ui.photos.photos]
            self.ai_thread = Engine(paths)
        else:
            paths = [os.path.normpath(i.path) for i in self.ui.photos.photos[begin: end]]
            self.ai_thread = Engine(paths, begin)
            
        self.ai_thread.started.connect(self.on_started)
        self.ai_thread.finished.connect(self.on_finished)
        self.ai_thread.aisignal.connect(self.on_change, QtCore.Qt.QueuedConnection)
        if not self.ai_thread.isRunning():
            self.ai_thread.start()
            
    def on_stop(self):
        self.ai_thread.running = False
        self.ui.timer.on_clicked(self.states['stopped_by_user'])
        self.ui.btn_stop.setEnabled(False)
        
    def on_started(self):
        print('Вызван метод on_started()')
        self.ui.label_info.setText(self.states['ai_started'])
        self.ui.blocker.blockAll('block')
        self.ui.btn_stop.setEnabled(True)
        self.ui.progressBar.setValue(0)
        
    def on_finished(self):
        self.ui.blocker.blockAll('unblock')
        self.ui.btn_stop.setEnabled(False)
        print('Вызван метод on_finished()')
        
    def on_change(self, index, progress, s):
        if s == 'AppError':
            QMessageBox.warning(self.ui, self.states["error_title"], self.states["error_message"])
            self.on_stop()
        else:
            self.ui.progressBar.setValue(progress)
            self.ui.label_info.setText(self.translated_ai_number.format(index=index + 1))
            self.ui.photos.photos[index].textEdit_photo.insertPlainText(s)
    
    def combo_changed(self):
        value = self.ui.comboBox.currentText()
        if self.ui.photos.photos:
            if value == self.ui._translate('Describer', 'Все'):
                self.ui.comboBox_begin.setEnabled(False)
                self.ui.comboBox_end.setEnabled(False)
            else:
                self.ui.comboBox_begin.setEnabled(True)
                self.ui.comboBox_end.setEnabled(True)
        
    def end_change(self):
        self.end = self.ui.comboBox_end.currentText()
        self.get_begin_range()
        
    def get_begin_range(self):
        # определяем начало range'a
        begin = self.ui.comboBox_begin.currentText() or 1
        self.ui.comboBox_begin.clear()
        
        
        if begin and self.end:
            if int(begin) >= int(self.end) + 1:
                begin = 1
        
        if self.end:
            for i in range(1, int(self.end) + 1):
                self.ui.comboBox_begin.addItem(str(i))

        self.ui.comboBox_begin.setCurrentIndex(int(begin) - 1)
        
        self.begin = self.ui.comboBox_begin.currentText()
        
    def update_ranges(self):
        length = len(self.ui.photos.photos)
        end = self.ui.comboBox_end.currentText()
        
        self.ui.comboBox_end.clear()
        
        for i in range(1, length + 1):
            self.ui.comboBox_end.addItem(str(i))
        
        # определяем конец range'a
        if end and int(end) <= length:
            self.ui.comboBox_end.setCurrentIndex(int(end) - 1)
        else:
            self.ui.comboBox_end.setCurrentIndex(length - 1)
            
        self.end = self.ui.comboBox_end.currentText()
        
        self.get_begin_range()
        self.combo_changed()
            
        
            
        
        

            
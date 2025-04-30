import csv
import os
from PyQt5.QtWidgets import QFileDialog
from utils import load_api_keys, load_key_to_api

class CSVLoad(object):
    '''
    Сохранение и загрузка картинок из файла csv
    '''
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.conf = load_api_keys()
        self.last_path = self.conf['LAST_SAVE_PATH']
        
        self.ui.action_saveList.triggered.connect(self.save_csv)
        self.ui.action_loadList.triggered.connect(self.load_csv)
        
        self.ui.lang_changed.connect(self.retranslateUi)
        
    def retranslateUi(self):
        '''перевод'''
        self.suc_save = self.ui._translate('Describer', 'Файл {index} успешно сохранен!')
        self.save_list_files = self.ui._translate('Describer', 'Сохранить список файлов')
        self.type_doc = self.ui._translate('Describer', 'CSV Document *.csv')
        self.load_pics = self.ui._translate('Describer', 'Загрузить список картинок')
        
        self.states = {
            'fail_save': self.ui._translate('Describer', 'Не удалось сохранить файл'),
            'fail_load': self.ui._translate('Describer', 'Не удалось загрузить файл'),
            'success_csv': self.ui._translate('Describer', 'Список csv успешно загружен')
        }
        
        
    def save_csv(self):
        columns = ['index', 'path', 'description']
        items = [[i.number, os.path.normpath(os.path.abspath(i.path)), i.textEdit_photo.toPlainText()] for i in self.ui.photos.photos]
        
        try:
            file_path = QFileDialog.getSaveFileName(self.ui, self.save_list_files, self.last_path, self.type_doc)
            file_folder = os.path.dirname(os.path.abspath(file_path[0]))
            load_key_to_api('LAST_SAVE_PATH', file_folder)
            with open(file_path[0], 'w', encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(columns)
                for row in items:
                    writer.writerow(row)
            self.ui.timer.on_clicked(self.suc_save.format(index=file_path[0]), 5000)
        except Exception as e:
            self.ui.timer.on_clicked(self.ui._translate('Describer', self.states['fail_save']), 5000)
            print(e)
            
    def load_csv(self):
        file_path = QFileDialog.getOpenFileName(self.ui, self.load_pics, '', self.type_doc) # один формат
        if file_path[0]:
            try:
                self.ui.clear.delete_list()
                with open(file_path[0], 'r', encoding='utf-8') as f:
                    files = csv.reader(f)
                    paths, desc = list(zip(*[i[1:] for i in files][1:]))
                    self.ui.photos.register(paths, initial=1, desc=desc)
                    self.ui.numbers.initial_numbers()
                    self.ui.verticalLayout_photos.addSpacerItem(self.ui.photos.spacer)
                    self.ui.checker.check_photos()
                    self.ui.timer.on_clicked(self.states['success_csv'], 5000)
            except Exception as e:
                self.ui.timer.on_clicked(self.states['fail_load'], 5000)
                print(e)
        
            
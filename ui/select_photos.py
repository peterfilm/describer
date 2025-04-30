from utils.api import load_key_to_api, conf
from PyQt5.QtWidgets import QFileDialog
import os
import re

def natural_sort_key(s):
    '''
    Натуральный порядок чисел
    '''
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(r'(\d+)', s)]

class SelectPhotos:
    '''
    Кнопка открытия, добавление нескольких фотографий и папки
    '''
    def __init__(self, ui):
        self.ui = ui
        self.ui.action_openPictures.triggered.connect(self.select_clicked)
        self.ui.action_addPhotos.triggered.connect(self.add_clicked)
        self.ui.action_openFolder.triggered.connect(self.select_folder)
        
        self.ui.lang_changed.connect(self.retranslateUi)
        
    def retranslateUi(self):
        '''перевод'''
        self.states = {
            'fail_load': self.ui._translate('Describer', 'Не загрузить картинки'),
            'fail_add': self.ui._translate('Describer', 'Не удалось добавить картинки')
        }
        
    def get_photos(self):
        file_dialog = QFileDialog(self.ui)
        file_dialog.setOption(QFileDialog.ReadOnly)
        file_dialog.setOption(QFileDialog.HideNameFilterDetails)
        file_dialog.setNameFilters(conf['ALL_FORMATS'])
        
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        
        if file_dialog.exec_():
            return file_dialog.selectedFiles()
            
    def select_clicked(self):
        '''
        Выбираем картинки, затирая предыдущие
        '''
        selected_photos = self.get_photos()
        try:
            self.ui.photos.delete_photos()
            self.ui.photos.register(selected_photos)
            self.ui.numbers.initial_numbers()
            self.ui.verticalLayout_photos.addSpacerItem(self.ui.photos.spacer)
        except Exception as e:
            self.ui.timer.on_clicked(self.states['fail_load'], 5000)
            print(e)
        self.ui.checker.check_photos()
        
    def add_clicked(self):
        '''
        Добавляем фотографии в список
        '''
        selected_photos = self.get_photos()
        initial = len(self.ui.photos.photos) + 1
        try:
            self.ui.verticalLayout_photos.removeItem(self.ui.photos.spacer)
            self.ui.photos.register(selected_photos, initial)
            self.ui.numbers.add_numbers(initial)
            self.ui.verticalLayout_photos.addSpacerItem(self.ui.photos.spacer)
        except Exception as e:
            self.ui.timer.on_clicked(self.states['fail_add'], 5000)
            print(e)
        self.ui.checker.check_photos()
    
        
    def select_folder(self):
        '''
        Выбрать папку только с картинками
        '''
        try:
            folder_path = QFileDialog.getExistingDirectory(
                self.ui, 'Выберите папку', conf['LAST_PATH'])
            load_key_to_api('LAST_PATH', folder_path)
            files = self.get_files_by_extension(folder_path, conf['SELECTED_FORMATS'])
            
            self.ui.photos.delete_photos()
            self.ui.photos.register(files)
            self.ui.numbers.initial_numbers()
            self.ui.verticalLayout_photos.addSpacerItem(self.ui.photos.spacer)
        except Exception as e:
            self.ui.timer.on_clicked(self.states['fail_add'], 5000)
            print(e)
        self.ui.checker.check_photos()
    
    @staticmethod
    def get_files_by_extension(folder_path, extensions):
        '''
        Выбираем только файлы нужных форматов
        '''
        absolute_paths = []
        for file in os.listdir(folder_path):
            for extension in extensions:
                if file.lower().endswith(extension):
                    absolute_paths.append(os.path.join(folder_path, file))
                    break
        return sorted(absolute_paths, key=natural_sort_key)
            
        
        
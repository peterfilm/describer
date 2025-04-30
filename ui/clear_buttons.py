from PyQt5 import QtCore

class ClearAll(object):
    '''
    clear_fields - Очищает содержимое всех полей, не удаляя фотографии
    clear_list - удаляет сами фото
    '''
    def __init__(self, ui):
        self.ui = ui
        self.ui.btn_clear_all.clicked.connect(self.clear_fields)
        self.ui.action_clearAll.triggered.connect(self.delete_list)
        
        self.ui.lang_changed.connect(self.retranslateUi)
        
    def retranslateUi(self):
        '''перевод'''
        self.states = {
            "fields_cleaned": self.ui._translate('Describer', 'Текстовые поля успешно очищены'),
            "pictures_removed": self.ui._translate('Describer', 'Картинки удалены из очереди')
        }
        
    def clear_fields(self):
        for photo in self.ui.photos.photos:
            photo.textEdit_photo.clear()
            self.ui.timer.on_clicked(self.states["fields_cleaned"], 5000)
            
    def delete_list(self):
        self.ui.photos.delete_photos()
        self.ui.checker.check_photos()
        self.ui.timer.on_clicked(self.states['pictures_removed'], 5000)

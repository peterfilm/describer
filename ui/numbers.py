from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSignal


class Numbers(QObject):
    
    current_number = pyqtSignal()
    
    '''
    Combobox с количеством фотографий, при выборе изменяется обводка фотографий
    '''
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self._translate = QtCore.QCoreApplication.translate
        self.initial_numbers()
        self.ui.comboBox_number.currentTextChanged.connect(self.change_photo)
        
        self.ui.lang_changed.connect(self.retranslateUi)
        
    def retranslateUi(self):
        self.states = {
            'fail': self.ui._translate('Describer', 'Не обновить номера'),
        }
    
    def initial_numbers(self):
        if self.ui.photos.photos:
            for i, photo in enumerate(self.ui.photos.photos):
                self.ui.comboBox_number.addItem("")
                self.ui.comboBox_number.setItemText(i, self._translate("Describer", str(photo.number)))
            
    def add_numbers(self, number):
        if self.ui.photos.photos:
            for i in range(number, len(self.ui.photos.photos) + 1):
                self.ui.comboBox_number.addItem(str(i))
        
    def next_number(self):
        n = self.ui.comboBox_number.currentIndex()
        allPhotos = len(self.ui.photos.photos)
        self.ui.comboBox_number.setCurrentIndex((n + 1) % allPhotos)
        print(self.ui.comboBox_number.currentIndex())
            
    def change_photo(self):
        if self.ui.photos.photos:
            try:
                self.ui.photos.update_numbers()
                self.current_number.emit()
            except Exception as e:
                self.ui.timer.on_clicked(self.states['fail'], 5000)
                print(e)
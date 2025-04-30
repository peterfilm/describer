from PyQt5.QtCore import QObject, pyqtSignal
from utils import load_key_to_api, load_api_keys

class CopyPaste(QObject):
    copypaste_update = pyqtSignal()  # Объявление сигнала
    
    '''
    Checkbox определяющий будет ли вставка после нажатия или нет
    '''
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.conf = load_api_keys()
        self.ui.checkBox_copypaste.setChecked(self.conf['COPYPASTE'])
        self.ui.checkBox_copypaste.toggled.connect(self.change_checkbox)
        
    def change_checkbox(self):
        load_key_to_api('COPYPASTE', self.ui.checkBox_copypaste.isChecked())
        self.copypaste_update.emit()
        
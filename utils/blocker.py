from PyQt5.QtCore import QObject, pyqtSignal

class Blocker(QObject):
    '''
    Блокирует все кнопки
    '''
    block_All = pyqtSignal(str) 
    
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        
    def blockAll(self, signal):
        self.block_All.emit(signal)
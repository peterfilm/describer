from PyQt5.QtWidgets import QMainWindow, QApplication
import sys
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
import os
from ui import *
from utils import Checker, ClipboardWorker, Blocker, load_api_keys, load_key_to_api
from PyQt5.QtCore import pyqtSignal
from functools import partial

class AiDescriber(QMainWindow, Ui_Describer):
    swap_signal = pyqtSignal()
    lang_changed = pyqtSignal(str)
    type_changed = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        # грузим qss в файл
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            qss_file_path = os.path.join(script_dir, "style.qss")
            with open(qss_file_path, "r") as qss_file:
                qss_content = qss_file.read()
            self.setStyleSheet(qss_content)
            
        except Exception as e:
            print(e)
            
        # грузим перевод
        self.translator = QtCore.QTranslator()
        self.conf = load_api_keys()
        self.current_language = self.conf['CURRENT_LANGUAGE']
        
        self.blocker = Blocker(self)
        self.working = False
        self._translate = QtCore.QCoreApplication.translate
        
        # Photos
        self.timer = Timer(self)
        
        self.setupUi(self)
        icon = QIcon(os.path.join("img", "icon.ico"))
        self.setWindowIcon(icon)
        self.copypaste = CopyPaste(self)
        
        self.photos = Photos(self)    
        
        self.count = Count(self)
        self.numbers = Numbers(self)
        self.shortcut = Shortcut(self)
        
        self.clipboard_worker = ClipboardWorker()
        self.addDesc = AddDescription(self)
        self.clear = ClearAll(self)
        self.select_photos = SelectPhotos(self)
        
        self.csvload = CSVLoad(self)

        self.ai = AI_description(self)
        self.checker = Checker(self) # проверяльщик 
        self.checker.check_photos() # выставляем начальные значения, если фотографий нет
        
        self.excel = Excel(self)
        
        
        self.pushButton_author.clicked.connect(self.open_modal_author)
        self.pushButton_settings.clicked.connect(self.open_settings)
        self.show()

        
    def set_language(self, language):
        """
        Устанавливает язык интерфейса.
        :param language: Код языка (например, 'ru', 'en').
        """
        if self.translator.load(f"translations/translate_{language}.qm"):
            QtCore.QCoreApplication.instance().installTranslator(self.translator)
            load_key_to_api('CURRENT_LANGUAGE', language)
            print(f"Установлен язык: {language}")
        else:
            print(f"Не удалось загрузить перевод для языка: {language}")
        
        # Обновляем интерфейс
        self.retranslateUi(self)
        self.lang_changed.emit(language)
        
    def changeEvent(self, event):
        """
        Переопределяем метод changeEvent для обработки изменения языка.
        """
        if event.type() == QtCore.QEvent.LanguageChange:
            self.retranslateUi(self)
        super().changeEvent(event)
        
    def open_settings(self):
        modal_dialog = SettingsWindow(self)
        modal_dialog.exec_()
        
    def open_modal_author(self):
        modal_dialog = PeterWindow(self)
        modal_dialog.exec_()



if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    # Создаем главное окно
    window = AiDescriber()
    window.show()

    # Устанавливаем язык (например, 'ru' или 'en')
    window.set_language(window.current_language)
    sys.exit(app.exec_())

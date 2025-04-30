from PyQt5.QtCore import QObject, pyqtSignal
from utils import load_api_keys
from PyQt5 import QtCore
import keyboard
     
        

class ShortcutWorker(QObject):
    """
    Рабочий класс для обработки нажатий клавиш в фоновом потоке.
    """
    shortcut_signal = pyqtSignal(str)  # Сигнал для передачи текста в основной поток

    def __init__(self, conf):
        super().__init__()
        self.conf = conf

    def start_listening(self):
        """
        Начинает прослушивание клавиш.
        """
        keyboard.on_press_key(self.conf['SHORTCUT'], self.handle_keypress, suppress=True)

    def handle_keypress(self, event):
        """
        Обрабатывает нажатие клавиши.
        """
        try:
            if event.scan_code == self.conf['SHORTCUT_CODE']:
                if (self.conf['SHORTCUT_KEYPAD'] == 'False' and not event.is_keypad) or \
                   (self.conf['SHORTCUT_KEYPAD'] == 'True' and event.is_keypad):
                    self.shortcut_signal.emit("next")  # Отправляем сигнал в основной поток
        except Exception as e:
            print(e)
            
            
class Shortcut:
    '''
    Кнопка шортката
    '''
    def __init__(self, ui):
        self.ui = ui
        self.it = iter(self.ui.photos.photos)
        self.conf = load_api_keys()
        self.copypaste = False

        # Создаем рабочий объект и поток
        self.worker_thread = QtCore.QThread()
        self.worker = ShortcutWorker(self.conf)
        self.worker.moveToThread(self.worker_thread)

        # Подключаем сигналы
        self.worker.shortcut_signal.connect(self.handle_shortcut)
        self.worker_thread.started.connect(self.worker.start_listening)

        # Запускаем поток
        self.worker_thread.start()
        
        # Подписываемся на сигнал обновления списка фотографий
        self.ui.copypaste.copypaste_update.connect(self.handle_copypaste)

    def __iter__(self):
        return self
    
    def __next__(self):
        try:
            return next(self.it)
        except StopIteration:
            print('Список закончился')
            self.renew_it()
            try:
                return next(self.it)
            except:
                pass

    def handle_shortcut(self, signal):
        """
        Обрабатывает сигнал из фонового потока.
        """
        if signal == "next":
            try:
                current_number = int(self.ui.comboBox_number.currentIndex())
                photo = self.ui.photos.photos[current_number]
                text = photo.textEdit_photo.toPlainText()
                self.ui.clipboard_worker.copy_text(text)
                self.ui.numbers.next_number()
                if self.copypaste:
                    keyboard.press_and_release('ctrl+v')
            except Exception as e:
                print(e)
                
    def handle_renew(self, signal):
        if signal == "update":
            self.renew_it()
            
    def handle_copypaste(self):
        cp = load_api_keys()
        self.copypaste = cp['COPYPASTE']
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtSignal

class ClipboardWorker(QObject):
    """
    Класс для работы с буфером обмена в основном потоке.
    """
    copy_signal = pyqtSignal(str)  # Сигнал для передачи текста в буфер обмена

    def __init__(self):
        super().__init__()
        self.copy_signal.connect(self.copy_to_clipboard)

    def copy_text(self, text):
        """
        Метод для отправки текста в буфер обмена через сигнал.
        """
        self.copy_signal.emit(text)

    def copy_to_clipboard(self, text):
        """
        Метод для копирования текста в буфер обмена.
        """
        clipboard = QApplication.clipboard()
        clipboard.clear(mode=clipboard.Clipboard)
        clipboard.setText(text, mode=clipboard.Clipboard)
from PyQt5.QtCore import QTimer

class Timer(object):
    '''
    Таймер после экшена
    '''
    
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.timer = QTimer()
        self.timer.timeout.connect(self.clear_label_text)
        
        
    def on_clicked(self, text, number = 2000):
        self.timer.stop()  # Stop the timer
        self.ui.label_info.setText(text)
        self.timer.start(number)  # Restart the timer
        
    def clear_label_text(self):
        if (hasattr(self.ui.ai, 'ai_thread') and self.ui.ai.ai_thread.isRunning()):
            # print("clear_label_text: Поток активен, пропускаем очистку")
            return
        if self.ui.working:
            return
        
        QTimer.singleShot(500, self._delayed_clear)  # Задержка 500 мс
        
    def _delayed_clear(self):
        # print("clear_label_text: Очищаем label_info и progressBar через задержку")
        self.ui.label_info.setText("")
        self.ui.progressBar.setValue(0)
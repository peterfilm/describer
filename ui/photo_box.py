from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImageReader
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QApplication
import os
import subprocess
from PyQt5.QtCore import QTimer
from engine import Engine
from utils import ClickableLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMessageBox
from utils import load_api_keys, load_key_to_api


class PhotoBox(object):
    def __init__(self, ui, path, number = 1, parent=None):
        self.ui = ui
        self.conf = load_api_keys()
        self.label = self.ui.label_info
        self.number = number
        self.progressBar = self.ui.progressBar
        self.path = os.path.normpath(path)
        self.folder = os.path.dirname(self.path)
        self.scrollBox = self.ui.scrollAreaWidgetContents
        self.name = os.path.basename(path)
        self.ai_thread = Engine(self.path)
        self.create_design()
        self.display_photo(path)
        
        self.ui.blocker.block_All.connect(self.block)
        self.ui.swap_signal.connect(self.check_active)
        
        self.ui.lang_changed.connect(self.retranslateUi)
        self.ui.type_changed.connect(self.change_type)
        
        # Текущие состояния
        
    def retranslateUi(self):
        """Обновляет переводы главного окна и дочернего виджета."""
        # Тексты
        self.ai_desc = self.ui._translate('Describer', 'Делаем AI описание фотографии № {number} - {name}')
        self.ai_desc_finish = self.ui._translate('Describer', 'Описание для фотографии № {number} - {name} готово!')
        
        self.label_number_photo.setText(self.ui._translate("Describer", f'№ {self.number}'))
        self.label_photo_name.setText(self.ui._translate("Describer", f'{self.name}'))
        self.pushButton_pic_open.setText(self.ui._translate("Describer", "Копировать"))
        self.pushButton_folder_open.setText(self.ui._translate("Describer", "Открыть папку"))
        self.pushButton_ai_desc.setText(self.ui._translate("Describer", "AI описание"))
        self.pushButton_del_pic.setText(self.ui._translate("Describer", "Убрать"))
        
        #tips
        self.label_photo_name.setToolTip(self.ui._translate('Describer', 'Скопировать путь к картинке'))
        self.photo.setToolTip(self.ui._translate('Describer', 'Открыть фотографию в просмотрщике'))
        
        # состояния
        self.states = {
            "opened_in_viewer": self.ui._translate('Describer', 'Файл открыт в проводнике'),
            "fail_viewer": self.ui._translate('Describer', 'Не удалось открыть файл в проводнике'),
            "copied_to_clipboard": self.ui._translate('Describer', 'Текст успешно скопирован в буфер обмена'),
            "failed_to_clipboard": self.ui._translate('Describer', 'Не удалось скопировать текст в буфер обмена'),
            "success_path_copy": self.ui._translate('Describer', 'Путь к файлу успешно скопирован в буфер обмена'),
            "fail_path_copy": self.ui._translate('Describer', 'Не удалось скопировать путь к файлу в буфер обмена'),
            "success_opened_folder": self.ui._translate('Describer', 'Папка с данной картинкой успешно открыта'),
            "fail_opened_folder": self.ui._translate('Describer', 'Не удалось открыть папку'),
            "photo_removed": self.ui._translate('Describer', 'Картинка успешно удалена из очереди'),
            "error_title": self.ui._translate('Describer', 'Ошибка'),
            "error_message": self.ui._translate('Describer', 'Закончились токены на HuggingFace. Ждите следующий день'),
        }
        
    def update_number(self, new_number):
        self.number = new_number
        self.label_number_photo.setText(f'№ {self.number}')
        
    def block(self, signal):
        if signal == 'block':
            self.pushButton_pic_open.setEnabled(False)
            self.pushButton_ai_desc.setEnabled(False)
            self.ui.btn_ai_describe.setEnabled(False)
        if signal == 'unblock':
            self.pushButton_pic_open.setEnabled(True)
            self.pushButton_ai_desc.setEnabled(True)
            self.ui.btn_ai_describe.setEnabled(True)
        
    def check_active(self):
        selected_value = self.ui.comboBox_number.currentText() or '1'
        if str(self.number) == selected_value:
            self.container.setObjectName("active")
        else:
            self.container.setObjectName("")
            
        # Принудительно обновляем стиль виджета
        self.container.style().unpolish(self.container)
        self.container.style().polish(self.container)
        self.container.update()
        
    def get_description(self):
        return self.textEdit_photo.toPlainText()
        
        
    def create_design(self):
        self.photo_layout = QtWidgets.QVBoxLayout()
        self.photo_layout.setContentsMargins(15, 5, 15, 15)
    
        self.container = QtWidgets.QWidget()  # Контейнер для группы
        self.container.setLayout(self.photo_layout)
        self.container.setMaximumSize(QtCore.QSize(16777215, 250))
        
        self.container.setProperty("photo_box_ref", self)
        
        self.photo_layout.setObjectName("photo_layout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        # номер фотографии
        self.label_number_photo = ClickableLabel(f'№ {self.number}',self.scrollBox)
        self.label_number_photo.setMinimumSize(QtCore.QSize(30, 0))
        self.label_number_photo.setMaximumSize(QtCore.QSize(150, 16777215))
        self.label_number_photo.clicked.connect(self.number_hover)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_number_photo.setFont(font)
        self.label_number_photo.setObjectName("label_number_photo")
        self.label_number_photo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_number_photo.setObjectName("number")
        self.horizontalLayout.addWidget(self.label_number_photo)
        
        #имя фотографии
        self.label_photo_name = ClickableLabel(self.scrollBox)
        self.label_photo_name.setMinimumSize(QtCore.QSize(0, 31))
        self.label_photo_name.setMaximumSize(QtCore.QSize(16777215, 31))
        
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.label_photo_name.setFont(font)
        self.label_photo_name.setObjectName("label_photo_name")
        self.label_photo_name.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_photo_name.clicked.connect(self.buffer_path)
        self.horizontalLayout.addWidget(self.label_photo_name)
        
        # кнопки перемещения - вверх
        self.button_up = QtWidgets.QPushButton(self.scrollBox)
        self.button_up.setMinimumSize(QtCore.QSize(25, 25))
        self.button_up.setMaximumSize(QtCore.QSize(25, 25))
        icon = QIcon("img/up_arrow_yellow.png")  # Путь к вашему PNG-файлу
        self.button_up.setIconSize(QSize(15, 8))
        self.button_up.setIcon(icon)
        self.button_up.setText("")  # Очищаем текст
        self.button_up.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.horizontalLayout.addWidget(self.button_up)
        
        # кнопки перемещения - вниз
        self.button_down = QtWidgets.QPushButton(self.scrollBox)
        self.button_down.setMinimumSize(QtCore.QSize(25, 25))
        self.button_down.setMaximumSize(QtCore.QSize(25, 25))
        icon = QIcon("img/down_arrow_yellow.png")  # Путь к вашему PNG-файлу
        self.button_down.setIconSize(QSize(15, 8))
        self.button_down.setIcon(icon)
        self.button_down.setText("")  # Очищаем текст
        self.button_down.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.horizontalLayout.addWidget(self.button_down)
        
        self.photo_layout.addLayout(self.horizontalLayout)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_n = QtWidgets.QHBoxLayout()
        self.horizontalLayout_n.setObjectName("horizontalLayout_n")
        
        # фотография
        self.photo = ClickableLabel(self.scrollBox)
        self.photo.setMinimumSize(QtCore.QSize(150, 100))
        self.photo.setMaximumSize(QtCore.QSize(150, 150))
        self.photo.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.photo.setObjectName("photo")
        self.photo.clicked.connect(lambda: self.open_image_viewer())
        self.horizontalLayout_n.addWidget(self.photo)
        
        # текстовое поле
        self.textEdit_photo = QtWidgets.QTextEdit(self.scrollBox)
        self.textEdit_photo.setMinimumSize(QtCore.QSize(0, 150))
        self.textEdit_photo.setMaximumSize(QtCore.QSize(16777215, 150))
        self.textEdit_photo.setObjectName("textEdit_photo")
        self.horizontalLayout_n.addWidget(self.textEdit_photo)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_n)
        
        self.change_type(self.conf['CURRENT_TYPE'])
        
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        
        
        # Кнопка копировать текст
        self.pushButton_pic_open = QtWidgets.QPushButton(self.scrollBox)
        self.pushButton_pic_open.setMinimumSize(QtCore.QSize(120, 31))
        self.pushButton_pic_open.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_pic_open.setObjectName("pushButton_pic_open")
        self.pushButton_pic_open.clicked.connect(self.buffer)
        self.verticalLayout.addWidget(self.pushButton_pic_open)
        
        # Кнопка открыть папку
        self.pushButton_folder_open = QtWidgets.QPushButton(self.scrollBox)
        self.pushButton_folder_open.setMinimumSize(QtCore.QSize(120, 31))
        self.pushButton_folder_open.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_folder_open.setObjectName("pushButton_folder_open")
        self.pushButton_folder_open.clicked.connect(self.open_folder)
        self.verticalLayout.addWidget(self.pushButton_folder_open)
        
        # Кнопка AI описания
        self.pushButton_ai_desc = QtWidgets.QPushButton(self.scrollBox)
        self.pushButton_ai_desc.setMinimumSize(QtCore.QSize(120, 31))
        self.pushButton_ai_desc.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_ai_desc.setObjectName("pushButton_ai_desc")
        self.verticalLayout.addWidget(self.pushButton_ai_desc)
        
        # обработка нажатой кнопки
        self.pushButton_ai_desc.clicked.connect(self.ai_describe)
        self.ai_thread.started.connect(self.on_started)
        self.ai_thread.finished.connect(self.on_finished)
        self.ai_thread.aisignal.connect(self.on_change, QtCore.Qt.QueuedConnection)
        
        # Кнопка убрать из списка
        self.pushButton_del_pic = QtWidgets.QPushButton(self.scrollBox)
        self.pushButton_del_pic.setMinimumSize(QtCore.QSize(120, 31))
        self.pushButton_del_pic.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_del_pic.setObjectName("pushButton_del_pic")
        self.verticalLayout.addWidget(self.pushButton_del_pic)
        self.horizontalLayout_6.addLayout(self.verticalLayout)
        self.photo_layout.addLayout(self.horizontalLayout_6)
        self.pushButton_del_pic.clicked.connect(self.del_pic)
            
        self.button_up.clicked.connect(self.change_up)
        self.button_down.clicked.connect(self.change_down)
        
        self.retranslateUi()
        self.check_active()
        
    def get_photo_box_from_widget(self, widget):
        """
        Возвращает объект PhotoBox, связанный с виджетом.
        """
        return widget.property("photo_box_ref")
    
        
    def display_photo(self, path):
        '''
        Показываем фотографию корректно независимо от ее размеров
        '''
        image_reader = QImageReader(path)
        image_reader.setAutoTransform(True)
        image = image_reader.read()
        pixmap = QPixmap.fromImage(image)
        pixmap = pixmap.scaled(150, 150, aspectRatioMode=Qt.KeepAspectRatio)
        self.photo.setPixmap(pixmap)
        self.photo.setAlignment(Qt.AlignCenter)
        
    def open_image_viewer(self):
        '''
        Открыть файл в проводнике
        '''
        try:
            url = QUrl.fromLocalFile(self.path)
            QDesktopServices.openUrl(url)
            self.ui.timer.on_clicked(self.states['opened_in_viewer'], 5000)
        except:
            self.ui.timer.on_clicked(self.states['fail_viewer'], 5000)
        
    def buffer(self):
        '''
        Скопировать текст в буфер обмена
        '''
        try:
            a = self.textEdit_photo.toPlainText()
            cb = QApplication.clipboard()
            cb.clear(mode=cb.Clipboard)
            cb.setText(a, mode=cb.Clipboard)
            self.ui.timer.on_clicked(self.states['copied_to_clipboard'], 5000)
        except:
            self.ui.timer.on_clicked(self.states['failed_to_clipboard'], 5000)
        
    def buffer_path(self):
        '''
        Скопировать путь фотографии в буфер обмена
        '''
        try:
            cb = QApplication.clipboard()
            cb.clear(mode=cb.Clipboard)
            cb.setText(os.path.abspath(self.path), mode=cb.Clipboard)
            self.ui.timer.on_clicked(self.states['success_path_copy'], 5000)
        except:
            self.ui.timer.on_clicked(self.states['fail_path_copy'], 5000)
        
    def open_folder(self):
        '''
        Открыть папку с фотографией и выделить ее
        '''
        try:
            if os.name == "nt":  # Windows
                subprocess.Popen(["explorer", "/select,", os.path.normpath(self.path)])
            elif os.name == "posix":  # macOS or Linux
                subprocess.Popen(["xdg-open", os.path.normpath(folder_path)])
            else:
                print("Unsupported operating system.")
            self.ui.timer.on_clicked(self.states['success_opened_folder'], 5000)
        except Exception as e:
            print("Error opening folder:", e)
            self.ui.timer.on_clicked(self.states['fail_opened_folder'], 5000)
            
    def ai_describe(self):
        if not self.ai_thread.isRunning():
            self.ai_thread.start()
        
    def on_started(self):
        self.ui.blocker.blockAll('block')
        self.textEdit_photo.clear()
        self.label.setText(self.ai_desc.format(number=self.number, name=self.name))
        self.progressBar.setValue(50)
        self.ai_thread.running = False
        self.ui.working = True
        print('Вызван метод on_started()')
        
    def on_finished(self): # Вызывается при завершении потока
        print('Вызван метод on_finished()')
        self.ui.working = False
        self.ui.blocker.blockAll('unblock')
        self.progressBar.setValue(100)
        self.ai_thread.running = False
        self.ui.timer.on_clicked(self.ai_desc_finish.format(number=self.number, name=self.name))
        
    def on_change(self, index, progress, s):
        if s == 'AppError':
            QMessageBox.warning(self.ui, self.states["error_title"], self.states["error_message"])
        else:
            self.textEdit_photo.insertPlainText(s)
        
    def closeEvent(self, event): # Вызывается при закрытии окна
        self.hide() # Скрываем окно
        self.ai_thread.running = False # Изменяем флаг выполнения
        self.ai_thread.wait(5000) # Даем время, чтобы закончить
        event.accept()
        
    def clear_label_text(self):
        self.label.setText("")
        self.progressBar.setValue(0)
    
    def number_hover(self):
        self.ui.comboBox_number.setCurrentIndex(self.number - 1)
        self.ui.photos.update_numbers()
            
        
        
    def del_pic(self):
        self.ui.photos.delete_photo(self.number)
        self.ui.timer.on_clicked(self.states['photo_removed'], 5000)
        
    def change_up(self):
        if self.ui.photos.photos:
            self.ui.photos.swap_photos_up(self.number)
            
    def change_down(self):
        if self.ui.photos.photos:
            self.ui.photos.swap_photos_down(self.number)
            
    def change_type(self, size):
        font = self.textEdit_photo.font()
        font.setPointSize(size)
        self.textEdit_photo.setFont(font)
        
        
    def __repr__(self):
        return f'Photobox({self.name}, {self.number})'
    
    def __str__(self):
        return f'Photobox({self.name}, {self.number})'
        
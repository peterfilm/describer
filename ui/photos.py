from ui.photo_box import PhotoBox
from PyQt5 import QtWidgets
import os
from PyQt5.QtCore import QObject, pyqtSignal
    

class Photos(QObject):
    photos_updated = pyqtSignal()
    
    
    def __init__(self, ui, lst = None):
        super().__init__() 
        self.photos = []
        self.ui = ui
        # Кевин Спейсер
        self.spacer = QtWidgets.QSpacerItem(20, 176, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.ui.lang_changed.connect(self.retranslateUi)
        self.retranslateUi()
        if lst != None:
            self.register(lst)
            
        self.ui.verticalLayout_photos.addSpacerItem(self.spacer)
        
                    
    def retranslateUi(self):
        '''перевод'''
        self.states = {
            'removed_from_queque': self.ui._translate('Describer', 'Картинка успешно удалена из очереди'),
            'removed_from_queque_all': self.ui._translate('Describer', 'Картинки успешно удалена из очереди'),
            'fail': self.ui._translate('Describer', 'Не удалось удалить картинку'),
            'load_photos': self.ui._translate("Describer", "Загружаю фотографию"),
            'photos_load': self.ui._translate('Describer', 'Картинки успешно загружены')
        }

    def delete_photo(self, number):
        try:
            photo = next((p for p in self.photos if p.number == number), None)
            parent_widget = photo.photo_layout.parentWidget()
            if parent_widget:
                
                if hasattr(photo, "disconnect_signals"):
                    photo.disconnect_signals()
                        
                self.ui.verticalLayout_photos.removeWidget(parent_widget)
                parent_widget.deleteLater()
                self.photos.remove(photo)
                self.ui.comboBox_number.removeItem(self.ui.comboBox_number.count() - 1)
            self.update_numbers()
            self.ui.checker.check_photos()
            if not self.ui.photos.photos:
                self.ui.verticalLayout_photos.removeItem(self.spacer)
            self.photos_updated.emit()
            self.ui.timer.on_clicked(self.states['removed_from_queque'], 5000)
            self.disable_navigator()
        except Exception as e:
            self.ui.timer.on_clicked(self.states['fail'], 5000)
            print(e)
    
    def delete_photos(self):
        try:
            self.ui.verticalLayout_photos.removeItem(self.spacer)
            
            for photo in self.photos:
                parent_widget = photo.photo_layout.parentWidget()
                if parent_widget:
                    if hasattr(photo, "disconnect_signals"):
                        photo.disconnect_signals()
                    
                    self.ui.verticalLayout_photos.removeWidget(parent_widget)
                    parent_widget.deleteLater()
                    self.ui.comboBox_number.removeItem(self.ui.comboBox_number.count() - 1)
                    
            self.photos.clear()
            self.photos_updated.emit()
            self.ui.comboBox_ai.model().item(2).setEnabled(False)
            self.ui.timer.on_clicked(self.states['removed_from_queque_all'], 5000)
            
            # self.print_layout_contents(self.ui.verticalLayout_photos)
        except Exception as e:
            self.ui.timer.on_clicked(self.states['fail'], 5000)
            print(e)
        
    def update_numbers(self):
        for i, photo in enumerate(self.photos, 1):
            photo.update_number(i)
            photo.check_active()
            
    def disable_navigator(self):
        # блокируем кнопку навигации у первой и последней картинки
        if self.photos:
            self.photos[0].button_up.setDisabled(True)
            self.photos[len(self.photos) - 1].button_down.setDisabled(True)
            
    def enable_navigator(self):
        # блокируем кнопку навигации у первой и последней картинки
        if self.photos:
            self.photos[len(self.photos) - 1].button_down.setEnabled(True)
            
    def print_layout_contents(self, layout):
        '''
        отладочный принт, чтобы проверить какие элементы являются виджетами, какие нет
        '''
        print(f"Количество элементов в layout: {layout.count()}")
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    print(f"Элемент {i}: {widget} (тип: {type(widget)})")
                else:
                    print(f"Элемент {i}: не является виджетом", type(widget))
            else:
                print(f"Элемент {i}: отсутствует")
            
    def swap_photos_up(self, number):
        n1 = number - 1
        n2 = number - 2
        
        if n1 >= 1:
            
            widget1 = self.ui.verticalLayout_photos.itemAt(n1).widget()
            widget2 = self.ui.verticalLayout_photos.itemAt(n2).widget()
            
            if widget1 is None or widget2 is None:
                print("Ошибка: один из виджетов отсутствует в layout'е.")
                return
            
            
            # Получаем объекты PhotoBox
            photo_box1 = self.photos[n1].get_photo_box_from_widget(widget1)
            photo_box2 = self.photos[n2].get_photo_box_from_widget(widget2)
            
            photo_box1.button_up.setEnabled(True)
            photo_box2.button_up.setEnabled(True)
            
            photo_box1.button_down.setEnabled(True)
            photo_box2.button_down.setEnabled(True)
            
            # Меняем местами атрибуты объектов
            photo_box1.number, photo_box2.number = photo_box2.number, photo_box1.number
            
            # Обновляем интерфейс для каждого виджета
            self.update_widget(photo_box1)
            self.update_widget(photo_box2)
            
            self.ui.verticalLayout_photos.removeWidget(widget1)
            self.ui.verticalLayout_photos.removeWidget(widget2)

            self.ui.verticalLayout_photos.insertWidget(n2, widget1)
            self.ui.verticalLayout_photos.insertWidget(n1, widget2)
            
            # Обновляем порядок объектов в списке self.photos
            self.photos[n1], self.photos[n2] = self.photos[n2], self.photos[n1]
            self.ui.swap_signal.emit()
            self.disable_navigator()
            
    
    def swap_photos_down(self, number):
        n1 = number - 1
        n2 = number
        
        if n2 < len(self.photos):
            
            widget1 = self.ui.verticalLayout_photos.itemAt(n1).widget()
            widget2 = self.ui.verticalLayout_photos.itemAt(n2).widget()
            
            # Получаем объекты PhotoBox
            photo_box1 = self.photos[n1].get_photo_box_from_widget(widget1)
            photo_box2 = self.photos[n2].get_photo_box_from_widget(widget2)
            
            photo_box1.button_up.setEnabled(True)
            photo_box2.button_up.setEnabled(True)
            
            photo_box1.button_down.setEnabled(True)
            photo_box2.button_down.setEnabled(True)
            
            
            # Меняем местами атрибуты объектов
            photo_box1.number, photo_box2.number = photo_box2.number, photo_box1.number
            
            # Обновляем интерфейс для каждого виджета
            self.update_widget(photo_box1)
            self.update_widget(photo_box2)
            
            self.ui.verticalLayout_photos.removeWidget(widget1)
            self.ui.verticalLayout_photos.removeWidget(widget2)

            self.ui.verticalLayout_photos.insertWidget(n1, widget2)
            self.ui.verticalLayout_photos.insertWidget(n2, widget1)
            
            # Обновляем порядок объектов в списке self.photos
            self.photos[n1], self.photos[n2] = self.photos[n2], self.photos[n1]
            
            self.ui.swap_signal.emit()
            self.disable_navigator()
            
    def update_widget(self, photo_box):
        """
        Обновляет интерфейс виджета на основе данных объекта PhotoBox.
        """
        if hasattr(photo_box, "label"):  # Если есть QLabel
            photo_box.label_number_photo.setText(f"№ {photo_box.number}")
            
    def register(self, lst, initial=1, desc=None):
        self.enable_navigator()
        old = len(self.photos)
        for i, path in enumerate(lst, initial):
            photo = PhotoBox(self.ui, path, i)
            if desc:
                photo.textEdit_photo.insertPlainText(desc[i - 1])
            self.ui.progressBar.setValue(int(((i - old) / len(lst)) * 100))
            self.ui.label_info.setText(f'{self.states["load_photos"]} {os.path.basename(path)}')
            self.photos.append(photo)
            self.ui.verticalLayout_photos.addWidget(photo.container)
        self.disable_navigator()
        self.photos_updated.emit() 
        self.ui.verticalLayout_photos.update()
        self.ui.verticalLayout_photos.activate()
        
        self.ui.timer.on_clicked(self.states['photos_load'], 5000)
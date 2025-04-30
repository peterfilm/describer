from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QPixmap, QImageReader
from PyQt5.QtCore import Qt
from utils import ClickableLinkLabel
from utils import load_api_keys, load_key_to_api
from PyQt5.QtCore import pyqtSignal
from utils import is_valid_token
from PyQt5.QtWidgets import QMessageBox

class SettingsWindow(QDialog):
    '''
    Окошко об авторе
    '''
    token_check = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.ui = parent
        self._translate = QtCore.QCoreApplication.translate
        self.conf = load_api_keys()
        self.langs = self.conf['LANGUAGES']
        self.lang_now = self.conf['CURRENT_LANGUAGE']
        self.engines = self.conf['ENGINE']
        self.engine_now = self.conf['CURRENT_ENGINE']
        self.token = self.conf['TOKEN']
        self.setupUi()
        self.checker()
        self.parent = parent
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        
        # Actions
        self.comboBox_language.currentTextChanged.connect(self.lang_changed)
        self.comboBox_engine.currentTextChanged.connect(self.engine_changed)
        self.lineEdit_token.returnPressed.connect(self.token_changed)
        
        self.spinBox_typeSize.valueChanged.connect(self.type_changed)
        self.spinBox_min.valueChanged.connect(self.min_changed)
        self.spinBox_max.valueChanged.connect(self.max_changed)
        
        self.token_check.connect(self.checker)
        self.comboBox_description.currentTextChanged.connect(self.engine_type_changed)
        
    def setupUi(self):
        self.setObjectName("Dialog")
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.resize(500, 450)
        self.setMinimumSize(QtCore.QSize(500, 450))
        self.setMaximumSize(QtCore.QSize(500, 450))
        self.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.setSizeGripEnabled(False)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.label = QtWidgets.QLabel()
        self.label.setMinimumSize(QtCore.QSize(0, 31))
        self.label.setMaximumSize(QtCore.QSize(16777215, 31))
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        
        self.label_engine = QtWidgets.QLabel()
        self.label_engine.setMinimumSize(QtCore.QSize(0, 31))
        self.label_engine.setMaximumSize(QtCore.QSize(16777215, 31))
        self.label_engine.setObjectName("label")
        self.verticalLayout.addWidget(self.label_engine)
        
        self.label_4 = QtWidgets.QLabel()
        self.label_4.setMinimumSize(QtCore.QSize(0, 31))
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 31))
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label_2 = QtWidgets.QLabel()
        self.label_2.setMinimumSize(QtCore.QSize(0, 31))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 31))
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel()
        self.label_3.setMinimumSize(QtCore.QSize(0, 31))
        self.label_3.setMaximumSize(QtCore.QSize(16777215, 31))
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_5 = QtWidgets.QLabel()
        self.label_5.setMinimumSize(QtCore.QSize(0, 31))
        self.label_5.setMaximumSize(QtCore.QSize(16777215, 31))
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel()
        self.label_6.setMinimumSize(QtCore.QSize(120, 31))
        self.label_6.setMaximumSize(QtCore.QSize(16777215, 31))
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        self.comboBox_language = QtWidgets.QComboBox()
        self.comboBox_language.setMinimumSize(QtCore.QSize(0, 31))
        self.comboBox_language.setMaximumSize(QtCore.QSize(16777215, 31))
        self.comboBox_language.setObjectName("comboBox_language")
        self.verticalLayout_2.addWidget(self.comboBox_language)
        
        self.comboBox_engine = QtWidgets.QComboBox()
        self.comboBox_engine.setMinimumSize(QtCore.QSize(0, 31))
        self.comboBox_engine.setMaximumSize(QtCore.QSize(16777215, 31))
        self.comboBox_engine.setObjectName("comboBox_engine")
        self.verticalLayout_2.addWidget(self.comboBox_engine)
        
        
        self.spinBox_typeSize = QtWidgets.QSpinBox()
        self.spinBox_typeSize.setMinimumSize(QtCore.QSize(0, 31))
        self.spinBox_typeSize.setMaximumSize(QtCore.QSize(16777215, 31))
        self.spinBox_typeSize.setObjectName("spinBox_typeSize")
        self.spinBox_typeSize.setMinimum(1)
        self.spinBox_typeSize.setValue(self.conf['CURRENT_TYPE'])
        
        self.verticalLayout_2.addWidget(self.spinBox_typeSize)
        self.lineEdit_token = QtWidgets.QLineEdit()
        self.lineEdit_token.setMinimumSize(QtCore.QSize(0, 31))
        self.lineEdit_token.setMaximumSize(QtCore.QSize(16777215, 31))
        self.lineEdit_token.setObjectName("lineEdit_token")
        self.lineEdit_token.setText(self.token)
        self.verticalLayout_2.addWidget(self.lineEdit_token)
        self.comboBox_description = QtWidgets.QComboBox()
        self.comboBox_description.setMinimumSize(QtCore.QSize(0, 31))
        self.comboBox_description.setMaximumSize(QtCore.QSize(16777215, 31))
        self.comboBox_description.setObjectName("comboBox_description")
        self.comboBox_description.addItem("")
        self.comboBox_description.addItem("")
        self.comboBox_description.addItem("")
        self.select_description()
        
        self.verticalLayout_2.addWidget(self.comboBox_description)
        self.spinBox_min = QtWidgets.QSpinBox()
        self.spinBox_min.setMinimumSize(QtCore.QSize(0, 31))
        self.spinBox_min.setMaximumSize(QtCore.QSize(16777215, 31))
        self.spinBox_min.setMinimum(5)
        self.spinBox_min.setObjectName("spinBox_min")
        self.spinBox_min.setValue(self.conf['MIN_CAPTION'])
        self.verticalLayout_2.addWidget(self.spinBox_min)
        self.spinBox_max = QtWidgets.QSpinBox()
        self.spinBox_max.setMinimumSize(QtCore.QSize(0, 31))
        self.spinBox_max.setMaximumSize(QtCore.QSize(16777215, 31))
        self.spinBox_max.setMinimum(15)
        self.spinBox_max.setMaximum(self.conf['MAX_LIMIT'])
        self.spinBox_max.setValue(self.conf['MAX_CAPTION'])
        self.spinBox_max.setObjectName("spinBox_max")
        self.verticalLayout_2.addWidget(self.spinBox_max)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.label_create_token = QtWidgets.QLabel()
        self.label_create_token.setMinimumSize(QtCore.QSize(0, 60))
        self.label_create_token.setMaximumSize(QtCore.QSize(16777215, 60))
        self.label_create_token.setAlignment(QtCore.Qt.AlignCenter)
        self.label_create_token.setObjectName("label_create_token")
        self.verticalLayout_3.addWidget(self.label_create_token)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_img_permission = QtWidgets.QLabel()
        self.label_img_permission.setMinimumSize(QtCore.QSize(254, 74))
        self.label_img_permission.setMaximumSize(QtCore.QSize(254, 74))
        self.label_img_permission.setAutoFillBackground(False)
        self.label_img_permission.setAlignment(QtCore.Qt.AlignCenter)
        self.label_img_permission.setWordWrap(False)
        self.label_img_permission.setObjectName("label_img_permission")
        self.horizontalLayout_2.addWidget(self.label_img_permission)
        self.label_link = ClickableLinkLabel('huggingface.co/settings/tokens', 'https://huggingface.co/settings/tokens', '#ffffff')
        self.label_link.setMinimumSize(QtCore.QSize(0, 24))
        self.label_link.setMaximumSize(QtCore.QSize(16777215, 24))
        self.label_link.setAlignment(QtCore.Qt.AlignCenter)
        self.label_link.setObjectName("label_link")
        self.horizontalLayout_2.addWidget(self.label_link)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        
        self.display_photo('img/hf_permission.jpg')

        self.retranslateUi()
        self.create_langs()
        self.create_engines()
        QtCore.QMetaObject.connectSlotsByName(self)
        
    def checker(self):
        if self.conf['TOKEN']:
            self.spinBox_min.setEnabled(True)
            self.spinBox_max.setEnabled(True)
            self.comboBox_description.model().item(1).setEnabled(True)
            self.comboBox_description.model().item(2).setEnabled(True)
        else:
            self.spinBox_min.setEnabled(False)
            self.spinBox_max.setEnabled(False)
            self.comboBox_description.model().item(1).setEnabled(False)
            self.comboBox_description.model().item(2).setEnabled(False)
        
    def display_photo(self, path):
        '''
        Показываем фотографию корректно независимо от ее размеров
        '''
        image_reader = QImageReader(path)
        image_reader.setAutoTransform(True)
        image = image_reader.read()
        pixmap = QPixmap.fromImage(image)
        pixmap = pixmap.scaled(254, 254, aspectRatioMode=Qt.KeepAspectRatio)
        self.label_img_permission.setPixmap(pixmap)
        self.label_img_permission.setAlignment(Qt.AlignCenter)
        
    def create_langs(self):
        if self.langs:
            counter = 1
            for i in range(len(self.langs)):
                self.comboBox_language.addItem("")
            for key, value in self.langs.items():

                if self.conf['LANGUAGES'][key]['code'] == self.lang_now:
                    self.comboBox_language.setItemText(0, self._translate("Describer", key))
                    continue
                else:
                    self.comboBox_language.setItemText(counter, self._translate("Describer", key))
                    counter += 1
                    
    def create_engines(self):
        if self.engines:
            counter = 1
            for i in range(len(self.engines)):
                self.comboBox_engine.addItem("")
            for key, value in self.engines.items():
                if self.conf['ENGINE'][key]['code'] == self.engine_now:
                    self.comboBox_engine.setItemText(0, self._translate("Describer", key))
                    continue
                else:
                    self.comboBox_engine.setItemText(counter, self._translate("Describer", key))
                    counter += 1
    
    def select_description(self):
        indx = self.conf['ENGINE_TYPE']
        self.comboBox_description.setCurrentIndex(indx)
    
    def engine_changed(self, asd):
        code = self.conf['ENGINE'][self.comboBox_engine.currentText()]['code']
        load_key_to_api('CURRENT_ENGINE', code)
        
    def engine_type_changed(self):
        item = int(self.comboBox_description.currentIndex())
        load_key_to_api('ENGINE_TYPE', item)
        
        
    def lang_changed(self):
        code = self.conf['LANGUAGES'][self.comboBox_language.currentText()]['code']
        self.ui.set_language(code)
        self.retranslateUi()
        
    def token_changed(self):
        text = self.lineEdit_token.text()
        if text == '':
            load_key_to_api('TOKEN', text)
        elif is_valid_token(text):
            load_key_to_api('TOKEN', text)
            QMessageBox.information(self, self._translate("Describer", "Токен изменен"), self._translate("Describer", "Токен успешно изменен"))
        else:
            QMessageBox.warning(self, self._translate("Describer", "Ошибка"), self._translate("Describer", "Некорректный токен"))
            self.lineEdit_token.setText('')
            load_key_to_api('TOKEN', '')
        self.conf = load_api_keys()
        self.token = text
        self.token_check.emit()
        
    def type_changed(self):
        load_key_to_api('CURRENT_TYPE', self.spinBox_typeSize.value())
        self.ui.type_changed.emit(self.spinBox_typeSize.value())
        
    def min_changed(self):
        smin = self.spinBox_min.value()
        smax = self.spinBox_max.value()
        load_key_to_api('MIN_CAPTION', smin)
        if smin >= smax:
            self.spinBox_max.setValue(smin + 15)
        
        self.spinBox_max.setMinimum(smin + 15)
        
    def max_changed(self):
        load_key_to_api('MAX_CAPTION', self.spinBox_max.value())
        
    

    def retranslateUi(self):
        self.setWindowTitle(self._translate("Describer", 'Настройки'))
        self.label.setText(self._translate("Describer", "Язык"))
        self.label_engine.setText(self._translate("Describer", "Движок"))
        self.label_4.setText(self._translate("Describer", "Шрифт"))
        self.label_2.setText(self._translate("Describer", "Huggingface API"))
        self.label_3.setText(self._translate("Describer", "Описание"))
        self.label_5.setText(self._translate("Describer", "Минимальная длина"))
        self.label_6.setText(self._translate("Describer", "Максимальная длина"))
        self.comboBox_description.setItemText(0, self._translate("Describer", "Полное описание"))
        self.comboBox_description.setItemText(1, self._translate("Describer", "Короткое описание"))
        self.comboBox_description.setItemText(2, self._translate("Describer", "Полное + короткое описание"))
        self.label_create_token.setText(self._translate("Describer", "Для того чтобы использовать короткое описание") + '\n - ' + self._translate("Describer", "зарегистрируйте токен здесь:"))

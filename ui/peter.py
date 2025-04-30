from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from utils import TextSelectableLabel, ClickableLinkLabel
import os

class PeterWindow(QDialog):
    '''
    Окошко об авторе
    '''

    def __init__(self, parent):
        super().__init__(parent)
        self.modal = PeterUI()
        self.modal.setupUi(self)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowModality(2)  # чтоб блокировало другие окна
        
class PeterUI(QtCore.QObject):
    def setupUi(self, Dialog):
        self._translate = QtCore.QCoreApplication.translate
        Dialog.setObjectName("Dialog")
        Dialog.resize(607, 197)
        Dialog.setMinimumSize(QtCore.QSize(607, 197))
        Dialog.setMaximumSize(QtCore.QSize(607, 197))
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(20, 20, 607, 155))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.qlabel_peterphoto = QtWidgets.QLabel(self.widget)
        self.qlabel_peterphoto.setMinimumSize(QtCore.QSize(151, 151))
        self.qlabel_peterphoto.setMaximumSize(QtCore.QSize(151, 151))
        self.qlabel_peterphoto.setStyleSheet("")
        self.qlabel_peterphoto.setText("")
        self.qlabel_peterphoto.setPixmap(
            QtGui.QPixmap(os.path.join("img", "pm.png")))
        self.qlabel_peterphoto.setObjectName("qlabel_peterphoto")
        self.verticalLayout.addWidget(self.qlabel_peterphoto)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setContentsMargins(15, -1, -1, -1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setMinimumSize(QtCore.QSize(0, 7))
        self.label.setGeometry(QtCore.QRect(0, 0, 500, 16))
        font = QtGui.QFont()
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.label_5 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)

        self.label_2 = ClickableLinkLabel(
            "peterfilm.ru", "https://peterfilm.ru", '#ffffff')
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setUnderline(True)
        font.setStrikeOut(False)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        
        
        self.label_fancy = ClickableLinkLabel(
            self._translate('Describer', "Создано на движке Huggingface"), "https://huggingface.co", '#ffffff')
        self.label_fancy.setFont(font)
        self.label_fancy.setObjectName("label_fancy")
        self.label_fancy.setGeometry(QtCore.QRect(0, 0, 400, 16))
        self.verticalLayout_2.addWidget(self.label_fancy)
        
        
        self.label_3 = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.label_4 = TextSelectableLabel(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        # self.retranslateUi(Dialog)
        # QtCore.QMetaObject.connectSlotsByName(Dialog)
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Describer", "Об Авторе"))
        self.label.setText(_translate(
            "Describer", "Программа создана нейронщиком для нейронщиков"))
        self.label_5.setText(_translate("Describer", "Автор: Петр Михайлуца"))
        self.label_3.setText(_translate(
            "Describer", "Если вы хотите поддержать проект:"))
        self.label_4.setText(_translate("Describer", "5536 9138 7123 3108"))

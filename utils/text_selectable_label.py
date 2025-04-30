from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor


class TextSelectableLabel(QLabel):
    '''
    в QLabel можно выделить текст
    '''

    def __init__(self, text):
        super().__init__(text)
        self.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.setCursor(QCursor(Qt.ArrowCursor))

    def enterEvent(self, event):
        self.setCursor(QCursor(Qt.IBeamCursor))

    def leaveEvent(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))
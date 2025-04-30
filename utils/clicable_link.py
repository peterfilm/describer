from PyQt5 import QtCore, QtWidgets
import os

class ClickableLinkLabel(QtWidgets.QLabel):
    
    def __init__(self, text, url, code = '#000000'):
        super().__init__()
        self.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.setOpenExternalLinks(True)
        self.setText(f'<a style="color: {code}" href="{url}">{text}</a>')
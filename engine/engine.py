from PyQt5 import QtCore
from random import random
import time
from utils import load_api_keys
from gradio_client import exceptions
from engine.fancyfeast_gradio import fancyfeast_gradio
from engine.florence import florence
from engine.florence_sd3 import florence_sd3
from engine.bart import short_caption
from utils import UnknownEngine, ServerError503

class Engine(QtCore.QThread):
    '''
    Принимает путь к файлу и возвращает описание 
    '''
    aisignal = QtCore.pyqtSignal(int, int, str)
    
    def __init__(self, paths, begin = 0, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.paths = paths
        self.running = False
        self.begin = begin
        self._translate = QtCore.QCoreApplication.translate
        
    def run(self):
        self.running = True
        while self.running:
            try:
                self.conf = load_api_keys()
                self.token = self.conf['TOKEN']
                self.model = self.conf['CURRENT_ENGINE']
                self.engine_type = self.conf['ENGINE_TYPE']
                self.min_length = self.conf['MIN_CAPTION']
                self.max_length = self.conf['MAX_CAPTION']
                if type(self.paths) == str:
                    # result = 'Описание из api ' + str(random())
                    match self.model:
                        case 'fancyfeast':
                            result = fancyfeast_gradio(self.paths, self.token)
                        case 'florence':
                            result = florence(self.paths, self.token)
                        case 'sd3':
                            result = florence_sd3(self.paths, self.token)
                        case _:
                            raise UnknownEngine(self._translate('Describer', 'Неизвестный движок'))
                    
                    if self.token:
                        match self.engine_type:
                            case 0:
                                pass
                            case 1:
                                result = short_caption(result, self.token, self.min_length, self.max_length)
                            case 2:
                                short_desc = short_caption(result, self.token, self.min_length, self.max_length)
                                separator = f'\n\n-------\n\n{self._translate("Describer", "Короткое описание:")}\n\n'
                                result += separator
                                result += short_desc
                    time.sleep(0.5)
                    self.aisignal.emit(0, 100, result)
                    self.running = False
                    
                if type(self.paths) == list:
                    for i, link in enumerate(self.paths, self.begin):
                        if not self.running:
                            break
                        # result = 'Описание из api ' + str(random())
                        match self.model:
                            case 'fancyfeast':
                                result = fancyfeast_gradio(link, self.token)
                            case 'florence':
                                result = florence(link, self.token)
                            case 'sd3':
                                result = florence_sd3(link, self.token)
                            case _:
                                raise UnknownEngine(self._translate('Describer', 'Неизвестный движок'))
                        
                        if self.token:
                            match self.engine_type:
                                case 0:
                                    pass
                                case 1:
                                    result = short_caption(result, self.token, self.min_length, self.max_length)
                                case 2:
                                    short_desc = short_caption(result, self.token, self.min_length, self.max_length)
                                    separator = f'\n\n-------\n\n{self._translate("Describer", "Короткое описание:")}\n\n'
                                    result += separator
                                    result += short_desc
                        progress = int((i - self.begin + 1) / len(self.paths) * 100)
                        self.aisignal.emit(i, progress, result)
                        time.sleep(0.5)
                    self.running = False
                    
            except exceptions.AppError as e:
                '''
                Ошибка, когда закончились токены
                '''
                self.aisignal.emit(0, 0, 'AppError')
                self.running = False
                
            except ServerError503 as e:
                self.aisignal.emit(0, 0, self._translate('Describer', 'Ошибка Сервера 503, попробуйте позже'))
                self.running = False
                    
            except Exception as e:
                print(e)
                self.aisignal.emit(0, 0, self._translate('Describer', 'Произошла ошибка!'))
                self.running = False
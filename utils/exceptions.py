class UnknownEngine(Exception):
    '''Ошибка, если неизвестный движок'''
    pass

class ServerError503(Exception):
    '''Ошибка сервера, попробуйте позже'''
    pass
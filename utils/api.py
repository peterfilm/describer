import json

def load_api_keys():
    '''
    Достаем файлы из настроек
    '''
    with open('config.json', encoding="utf-8") as file:
        data = json.load(file)
        return data


def load_key_to_api(name, value):
    '''
    Изменяем данные в настройках config.json
    name - ключ
    value - значение
    '''
    data = load_api_keys()
    data[name] = value
    with open('config.json', "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


conf = load_api_keys()
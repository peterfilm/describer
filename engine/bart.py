import requests
from huggingface_hub import InferenceClient
from utils.exceptions import ServerError503

def short_caption(text, token, min_length, max_length):
    print('bart started')
    # URL для запроса к модели
    api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    
    # Заголовки запроса
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Параметры запроса
    payload = {
        "inputs": text,
        "parameters": {
            "min_length": min_length,
            "max_length": max_length
        }
    }
    
    # Отправляем POST-запрос
    response = requests.post(api_url, headers=headers, json=payload)
    
    # Проверяем статус ответа
    if response.status_code == 200:
        result = response.json()
        return result[0]['summary_text']  # Извлекаем краткое описание
    else:
        print(f"Ошибка: {response.status_code}, {response.text}")
        raise ServerError503('Server Error') 

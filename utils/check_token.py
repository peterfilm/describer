from huggingface_hub import HfApi

def is_valid_token(token):
    try:
        api = HfApi()
        user_info = api.whoami(token=token)
        print(f"Токен принадлежит пользователю: {user_info['name']}")
        return True
    except Exception as e:
        print(f"Ошибка проверки токена: {e}")
        return False
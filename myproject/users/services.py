import requests
from requests import RequestException

from config.settings import BOT_TOKEN, TG_URL




def send_message_by_telegram(text, chat_id):
    """ Отправляет сообщение через Telegram """
    params = {
        'text': text,
        'chat_id': chat_id
    }
    try:
        response = requests.get(f'{TG_URL}{BOT_TOKEN}/sendMessage', params=params)
        response.raise_for_status()
    except RequestException as e:
        print(f'Ошибка при отправке  уведомления: {e}')

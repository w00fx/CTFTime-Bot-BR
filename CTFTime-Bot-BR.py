import json
import os
from botocore.vendored import requests
import time
from datetime import datetime
from dateutil import tz

URL_TELEGRAM = "https://api.telegram.org/bot{}/".format(os.environ['TELEGRAM_TOKEN'])

horario_atual = str(time.time()).split('.')[0]

URL_CTFTIME = 'https://ctftime.org/api/v1/events/?'
HEADERS = {'User-Agent': 'Mozilla/5.0'}
PARAMS = dict(
    limit='5',
    start=horario_atual,
    finish=str(int(horario_atual) + 2629800)
)


def send_message(text, chat_id):
    url = URL_TELEGRAM + "sendMessage?text={}&chat_id={}&parse_mode=markdown".format(text, chat_id)
    requests.get(url)


def convert_time(time):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/Sao_Paulo')
    utc = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')
    utc = utc.replace(tzinfo=from_zone)

    # Convert o fuso horario
    brasil = utc.astimezone(to_zone)
    brasil = brasil.strftime("%d/%m/%Y %H:%M")
    return brasil


def get_ctfs():
    resp = requests.get(URL_CTFTIME, params=PARAMS, headers=HEADERS)
    data = resp.json()
    mensagem = '*Próximos CTFs:*\n'
    for item in data:
        mensagem += '\n' + item['title']
        mensagem += '\nURL: ' + item['url']
        mensagem += '\nInicia em: ' + convert_time(item['start'][:19])
        mensagem += '\nTermina em: ' + convert_time(item['finish'][:19])
        mensagem += '\n'
    return mensagem


def handle(event, context):
    msg = event
    chat_id = msg['message']['chat']['id']
    command = msg['message']['text']
    if msg['message']['text']:
        if '/ctfs' in command[:5]:
            message = get_ctfs()
            send_message(message, chat_id)
            return '{"StatusCode": "200"}'

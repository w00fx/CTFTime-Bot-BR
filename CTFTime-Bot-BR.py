import requests
import daemon
import time
import telepot
from datetime import datetime
from dateutil import tz
from telepot.loop import MessageLoop


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
    resp = requests.get(URL, params=PARAMS, headers=HEADERS)
    data = resp.json()
    mensagem = '*Próximos CTFs:*\n'
    for item in data:
        mensagem += '\n' + item['title']
        mensagem += '\nURL: ' + item['url']
        mensagem += '\nInicia em: ' + convert_time(item['start'][:19])
        mensagem += '\nTermina em: ' + convert_time(item['finish'][:19])
        mensagem += '\n'
    return mensagem


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    if msg['text']:
        if '/ctfs' in command[:5]:
            bot.sendMessage(chat_id, get_ctfs(), parse_mode='Markdown')


horario_atual = str(time.time()).split('.')[0]

URL = 'https://ctftime.org/api/v1/events/?'
HEADERS = {'User-Agent': 'Mozilla/5.0'}
PARAMS = dict(
    limit='5',
    start=horario_atual,
    finish=str(int(horario_atual) + 2629800)
)

with daemon.DaemonContext():
    bot = telepot.Bot("SUA_BOT_API_AQUI")
    MessageLoop(bot, handle).run_as_thread()
    print('Estou escutando ...')
    while 1:
        time.sleep(10)

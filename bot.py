from pprint import pprint
from cqhttp import CQHttp

import random

bot = CQHttp(api_root='http://127.0.0.1:5700')


# 私聊消息
@bot.on_message('private')
def handle_msg(ctx):
    pprint(ctx)
    msg = ctx['message']
    if msg.startswitch('echo '):
        bot.send(ctx, msg[len('echo '):])
    elif msg == '':
        bot.send(ctx, 'm')
    elif msg == '':
        bot.send(ctx, str(random.randint(0, 100)))


bot.run('127.0.0.1', 8080)

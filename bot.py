from pprint import pprint
from cqhttp import CQHttp
import requests
import random

bot = CQHttp(api_root='http://127.0.0.1:5700')

commands = {}


def command(name):
    def decorator(func):
        commands[name] = func
        return func

    return decorator


@command('echo')
def echo(ctx, arg):
    return {'reply': arg}


@command('miaowing')
def miao(ctx, arg):
    return {'reply': 'miao'}


@command('随机数')
def rand(ctx, arg):
    return {'reply': str(random.randint(0, 100))}


@command('计算')
def calu(ctx, arg):
    expression = arg.strip()
    print(expression)
    return {'reply': str(eval(expression))}


@command('知乎日报')
def _(ctx, arg):
    STORY_URL_FORMAT = 'https://daily.zhihu.com/story/{}'

    resp = requests.get(
        'https://news-at.zhihu.com/api/4/news/latest',
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/71.0.3578.98 Safari/537.36 '
        }
    )

    data = resp.json()
    stories = data.get('stories')

    if not stories:
        bot.send(ctx, '暂时没有数据，或者服务无法访问')
        return

    reply = ''
    for story in stories:
        url = STORY_URL_FORMAT.format(story['id'])
        title = story.get('title', '未知内容')
        reply += f'\n{title}\n{url}\n'

    return {'reply': reply}


# print(commands) 测试打印内容：{'echo': <function echo at 0x000001A57EF87F78>}


# 私聊消息
@bot.on_message('group')
def handle_msg(ctx):
    pprint(ctx)
    msg: str = ctx['message']
    print(msg)
    sp = msg.split(maxsplit=1)
    print(sp)
    if not sp:
        return

    print(sp)
    cmd, *args = sp
    arg = ''.join(args)
    print('cmd:', cmd)
    print('arg:', arg)

    handler = commands.get(cmd)
    print('handler:', handler)

    if handler:
        return handler(ctx, arg)
    else:
        pass

    # if msg.startswith('echo '):
    #     # bot.send(ctx, msg[len('echo '):])
    #     return {'reply': msg[len('echo '):]}
    # elif msg == '':
    #     bot.send(ctx, 'm')
    # elif msg == '随机数':
    #     bot.send(ctx, str(random.randint(0, 100)))
    # elif msg.startswith('计算 '):
    #     expression = msg[len('计算 '):].strip()
    #     print(expression)
    #     # bot.send(ctx, message=str(eval(expression)))
    #     return {'reply': str(eval(expression))}


# import cmds

bot.run('127.0.0.1', 8080)

from aiohttp.web import Request, Response

import json
import os


CUR_DIT_DECONSTRUCTED: list = __file__.split('/')
APP_DIR: str = '/'.join(CUR_DIT_DECONSTRUCTED[0:len(CUR_DIT_DECONSTRUCTED)-2]) + '/models/'
NEWS_PATH: str = os.path.join(APP_DIR, 'news.json')
COMMENTS_PATH = os.path.join(APP_DIR, 'comments.json')

async def news_list(request: 'Request') -> 'Response':
    with open(NEWS_PATH, 'r') as f:
        news_dict: dict = json.loads(f.read())

    news_list: list = []

    for news in news_dict['news']:
        if news['deleted']:
            news_dict['news_count'] -= 1
        else:
            news_list.append(news)

    news_dict['news'] = news_list

    return Response(text=json.dumps(news_dict, indent=4))


async def news_detail(request):
    print(request)
    return Response(text='Ok')

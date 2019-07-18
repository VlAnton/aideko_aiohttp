from aiohttp.web import Request, Response

import json
import os


CUR_DIT_DECONSTRUCTED: list = __file__.split('/')
APP_DIR: str = '/'.join(CUR_DIT_DECONSTRUCTED[0:len(CUR_DIT_DECONSTRUCTED)-2]) + '/models/'
NEWS_PATH: str = os.path.join(APP_DIR, 'news.json')
COMMENTS_PATH = os.path.join(APP_DIR, 'comments.json')


def get_model_data(path):
    with open(path, 'r') as f:
        return json.loads(f.read())    

async def news_list(request: 'Request') -> 'Response':
    news_dict: dict = get_model_data(NEWS_PATH)

    news_list: list = []

    for news in news_dict['news']:
        if news['deleted']:
            news_dict['news_count'] -= 1
        else:
            news_list.append(news)

    news_dict['news'] = news_list

    return Response(text=json.dumps(news_dict, indent=4))


async def news_detail(request: 'Request') -> 'Response':
    try:
        news_item_id = int(str(request.rel_url)[1:])
        news_dict: dict = get_model_data(NEWS_PATH)

        if news_item_id not in set([news['id'] for news in news_dict['news']]):
            raise ValueError

    except ValueError:
        return Response(text='{\n\t"error": "news id is incorrect"\n}')

    comments_dict: dict = get_model_data(COMMENTS_PATH)

    news_item: dict = news_dict['news'][news_item_id-1]
    news_item['comments'] = []

    for comment in comments_dict['comments']:
        if comment['news_id'] == news_item_id:
            news_item['comments'].append(comment)

    return Response(text=json.dumps(news_item, indent=4))

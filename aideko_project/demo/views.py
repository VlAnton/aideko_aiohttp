from aiohttp.web import Request, Response

from iso8601 import parse_date

import json
import os


CUR_DIR_DECONSTRUCTED: list = __file__.split('/')
APP_DIR: str = '/'.join(CUR_DIR_DECONSTRUCTED[0:len(CUR_DIR_DECONSTRUCTED)-1]) + '/models/'
NEWS_PATH: str = os.path.join(APP_DIR, 'news.json')
COMMENTS_PATH = os.path.join(APP_DIR, 'comments.json')


def get_model_data(path):
    with open(path, 'r') as f:
        return json.loads(f.read())    


async def news_list(request: 'Request') -> 'Response':
    news_dict: dict = get_model_data(NEWS_PATH)
    news_list = list()

    for news in news_dict['news']:
        if news['deleted']:
            news_dict['news_count'] -= 1
        else:
            news_list.append(news)

    news_dict['news'] = news_list

    return Response(text=json.dumps(news_dict, indent=4))


def sort_by_date(item):
    return parse_date(item['date'])


def check_news_item(
        news_item_id: int,
        news_item: dict,
        news_list: list
        ) -> bool:
    ids: set = {news['id'] for news in news_list}

    id_not_exists: bool = news_item_id not in ids
    id_deleted: bool = news_item['deleted'] == True

    return id_not_exists or id_deleted


async def news_detail(request: 'Request') -> 'Response':
    try:
        news_item_id = int(str(request.rel_url)[1:])
        news_dict: dict = get_model_data(NEWS_PATH)
        news_item: dict = news_dict['news'][news_item_id-1]

        if check_news_item(news_item_id, news_item, news_dict['news']):
            raise ValueError

    except (ValueError, IndexError):
        return Response(
            text='{\n\t"error": "news id is incorrect or deleted"\n}',
            status=404
        )

    comments_dict: dict = get_model_data(COMMENTS_PATH)

    news_item['comments'] = list()
    news_item['comments_count'] = int()

    for comment in comments_dict['comments']:
        if comment['news_id'] == news_item_id:
            news_item['comments'].append(comment)
            news_item['comments_count'] += 1
    
    news_item['comments'].sort(key=sort_by_date)

    return Response(text=json.dumps(news_item, indent=4), status=200)

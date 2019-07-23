from aiohttp.web import Request, Response
from iso8601 import parse_date

import json

from .settings import NEWS_PATH, COMMENTS_PATH


def get_model_data(path, model):
    with open(path, 'r') as f:
        data = json.loads(f.read())
        print({item['id']:item for item in data[model]})
        return data

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

def retrieve_news_item(news_item_id: int, news_list: list) -> dict:
    for news_item in news_list:
        if news_item['id'] == news_item_id:
            return news_item


async def news_list(request: 'Request') -> 'Response':
    news_dict: dict = get_model_data(NEWS_PATH, 'news')
    news_list = list()

    for news_item in news_dict['news']:
        if news_item['deleted']:
            news_dict['news_count'] -= 1
        else:
            news_list.append(news_item)

    news_dict['news'] = news_list

    return Response(text=json.dumps(news_dict, indent=4))

async def news_detail(request: 'Request') -> 'Response':
    try:
        news_item_id = int(str(request.rel_url)[1:])
        news_list: list = get_model_data(NEWS_PATH, 'news')['news']
        news_item: dict = retrieve_news_item(news_item_id, news_list)

        if check_news_item(news_item_id, news_item, news_list):
            raise ValueError

    except (ValueError, IndexError):
        return Response(
            text='{\n\t"error": "news id is incorrect or deleted"\n}',
            status=404
        )

    comments_dict: dict = get_model_data(COMMENTS_PATH, 'comments')

    news_item['comments'] = list()
    news_item['comments_count'] = int()

    for comment in comments_dict['comments']:
        if comment['news_id'] == news_item_id:
            news_item['comments'].append(comment)
            news_item['comments_count'] += 1
    
    news_item['comments'].sort(key=sort_by_date)

    return Response(text=json.dumps(news_item, indent=4), status=200)

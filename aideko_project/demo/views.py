from aiohttp.web import Request, Response
from iso8601 import parse_date

import json

from .settings import NEWS_PATH, COMMENTS_PATH


def get_model_data(path: str, model: str) -> dict:
    with open(path, 'r') as f:
        data: dict = json.loads(f.read())
        return {item['id']:item for item in data[model]}

def sort_by_date(item: dict):
    return parse_date(item['date'])


async def news_list(request: 'Request') -> 'Response':
    news: dict = get_model_data(NEWS_PATH, 'news')
    news_response: dict = {
        'news': [],
        'news_count': 0
    }

    for news_item in news.values():
        if not news_item['deleted']:
            news_response['news_count'] += 1
            news_response['news'].append(news_item)

    return Response(text=json.dumps(news_response, indent=4))

async def news_detail(request: 'Request') -> 'Response':
    try:
        news_item_id = int(request.match_info['id'])
        news: dict = get_model_data(NEWS_PATH, 'news')
        news_item: dict = news.get(news_item_id)

        if not news_item or news_item['deleted'] == True:
            raise ValueError

    except ValueError:
        return Response(
            text='{\n\t"error": "news id is incorrect or deleted"\n}',
            status=404
        )

    comments_dict: dict = get_model_data(COMMENTS_PATH, 'comments')

    news_item['comments'] = list()
    news_item['comments_count'] = int()

    for comment in comments_dict.values():
        if comment['news_id'] == news_item_id:
            news_item['comments'].append(comment)
            news_item['comments_count'] += 1

    news_item['comments'].sort(key=sort_by_date)

    return Response(text=json.dumps(news_item, indent=4), status=200)

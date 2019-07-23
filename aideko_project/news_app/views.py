from .handlers import DataHandler, Response, json, NEWS_PATH


async def news_list(request: 'Request') -> 'Response':
    news: dict = DataHandler.get_model_data(NEWS_PATH)
    news_response: dict = {
        'news': [],
        'news_count': 0
    }

    for news_id, news_item in news.items():
        if not news_item['deleted'] and DataHandler.is_date(news_item['date']):
            DataHandler.set_comments(news_item, news_id)

            news_response['news_count'] += 1
            news_response['news'].append(news_item)

    news_response['news'].sort(key=DataHandler.sort_by_date)

    return Response(text=json.dumps(news_response, indent=4))


async def news_detail(request: 'Request') -> 'Response':
    news_id, news_item = DataHandler.retrieve_news_item(request)

    if isinstance(news_item, Response):
        return news_item

    news_item['comments'] = []
    news_item['comments_count'] = 0

    DataHandler.set_comments(news_item, news_id, is_detail=True)

    return Response(text=json.dumps(news_item, indent=4), status=200)

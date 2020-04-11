from datetime import datetime
from aiohttp.web import Response

import json

from .settings import NEWS_PATH, COMMENTS_PATH


class DataHandler:
    @classmethod
    def _parse_date(cls, date: str) -> 'datetime':
        return datetime.strptime(date, '%Y-%d-%mT%H:%M:%S')

    @classmethod
    def sort_by_date(cls, item: dict) -> 'datetime' or str:
        '''Преобразует строку в datetime. В случае неудачи возвращает строковое значение даты.'''
        try:
            date: 'datetime' = cls._parse_date(item['date'])
            return date
        except ValueError:
            return item['date']

    @classmethod
    def _get_comments_data(cls, data: dict):
        comments = {}

        for comment in data['comments']:
            news_id: int = comment['news_id']

            if not news_id in comments:
                comments[news_id] = [comment]
            else:
                comments[news_id].append(comment)
        return comments

    @classmethod
    def _get_news_data(cls, data: dict):
        return {item['id']:item for item in data['news']}

    @classmethod
    def get_model_data(cls, path: str) -> dict:
        '''
        Возвращает данные в следующем формате:
        — если хотим получить новости, то возвращаю их в формате {news_id: news_obj}
        — если комментарий, то {news_id: [list_of_comments_for_news_id]}
        '''
        with open(path, 'r') as f:
            data: dict = json.loads(f.read())

            if data.get('news'):
                return cls._get_news_data(data)
            return cls._get_comments_data(data)
    
    @classmethod
    def set_comments(cls, news_item: dict, news_id: int, is_detail=False) -> None:
        '''Задаёт значения для полей с комментариями к объекту новости в зависимости от вью'''
        comments: dict = cls.get_model_data(COMMENTS_PATH)

        if comments:
            comments_for_item: list or None = comments.get(news_id)

            if comments_for_item:
                comments_for_item = list(
                    filter(
                        lambda item: cls.is_date(item['date']),
                        comments_for_item
                    )
                )

                if is_detail:
                    comments_for_item.sort(key=cls.sort_by_date)
                    news_item['comments'] = comments_for_item
                news_item['comments_count'] = len(comments_for_item)
    
    @classmethod
    def is_date(cls, date: str) -> bool:
        try:
            date: 'datetime' = cls._parse_date(date)
        except ValueError:
            return False
        else:
            return date and date < datetime.now()

    @classmethod
    def retrieve_news_item(cls, request: 'Request') -> tuple:
        '''Получения новости по id. В случае неудачи возвращает tuple с ошибкой'''
        try:
            news_id = int(request.match_info['id'])
            news: dict = cls.get_model_data(NEWS_PATH)
            news_item: dict = news.get(news_id)

            if not (
                news_item and
                not news_item['deleted'] and
                cls.is_date(news_item['date'])
            ):
                raise ValueError
            return news_id, news_item

        except ValueError:
            response = Response(
                text='{\n\t"error": "news id is incorrect or deleted"\n}',
                status=404
            )
            return 0, response

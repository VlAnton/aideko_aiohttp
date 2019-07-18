from aiohttp.web import Application
from .views import news_list, news_detail


def setup_routes(app: 'Application') -> None:
    app.router.add_route('GET', '/', news_list)
    app.router.add_route('GET', '/{id}', news_detail)
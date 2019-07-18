from aiohttp.web import Application

from .views import frontend


def setup_routes(app: 'Application') -> None:
    app.router.add_route('GET', '/', frontend.news_list)
    app.router.add_route('GET', '/{id}', frontend.news_detail)
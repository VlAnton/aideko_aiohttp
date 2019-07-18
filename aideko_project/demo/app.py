from aiohttp.web import Application

from .routes import setup_routes


def create_app() -> 'Application':
    app = Application()
    setup_routes(app)

    return app
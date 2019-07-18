from aiohttp.web import Application

from .routes import setup_routes


async def create_app() -> 'Application':
    app = Application()
    setup_routes(app)

    return app
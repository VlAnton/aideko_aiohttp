import aiohttp
import aiohttp

from demo import create_app


app: 'Application' = create_app()

if __name__ == '__main__':
    aiohttp.web.run_app(app)

import aiohttp
import asyncio
# import aioreloader

from demo import create_app

# try:
#     import uvloop
#     asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
# except ImportError:
#     print('No such library: uvloop')



app: 'Application' = create_app()

if __name__ == '__main__':
    aiohttp.web.run_app(app)

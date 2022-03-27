from datetime import datetime

from aiohttp import web

start_datetime = datetime.now()


async def health(request: web.Request) -> web.Response:
    return web.Response(text='Everything ok!!!')


async def info(request: web.Request) -> web.Response:
    uptime = datetime.now() - start_datetime
    return web.Response(text=f'Server is up for {uptime} sec')

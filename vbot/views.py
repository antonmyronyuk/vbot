import logging
from datetime import datetime

from aiohttp import web

log = logging.getLogger(__name__)

start_datetime = datetime.now()


async def health(request: web.Request) -> web.Response:
    return web.Response(text='Everything ok!')


async def info(request: web.Request) -> web.Response:
    uptime = datetime.now() - start_datetime
    return web.Response(text=f'Server is up for {uptime} sec')


async def viber_hook(request: web.Request) -> web.Response:
    request_data = await request.json()
    log.info('Request data: %s', request_data)
    return web.json_response({'ok': True})

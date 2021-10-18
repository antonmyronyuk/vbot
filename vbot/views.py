from aiohttp import web


async def health(request: web.Request) -> web.Response:
    return web.Response(text='Everything ok!')

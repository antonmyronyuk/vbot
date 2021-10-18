import os

from aiohttp import web


async def health(request: web.Request) -> web.Response:
    return web.Response(text='Everything ok!')


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_route('GET', '/', health)
    app.router.add_route('GET', '/health', health)
    return app


def main() -> None:
    app = create_app()
    port = os.environ.get('PORT', 8080)
    web.run_app(app, port=port)

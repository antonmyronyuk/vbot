from aiohttp import web


async def health(request: web.Request) -> web.Response:
    return web.Response(text='Ok')


def create_app() -> web.Application:
    app = web.Application()
    app.router.add_route('GET', '/', health)
    app.router.add_route('GET', '/health', health)
    return app


def main() -> None:
    app = create_app()
    web.run_app(app)

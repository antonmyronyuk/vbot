import logging
import os

from aiohttp import web

from vbot import signals
from vbot import views

logging.basicConfig(level=logging.INFO)


def create_app() -> web.Application:
    app = web.Application()
    # app.on_startup.append(signals.start_ping)
    app.router.add_route('GET', '/', views.health)
    app.router.add_route('GET', '/health', views.health)
    app.router.add_route('GET', '/info', views.info)
    app.router.add_route('*', '/bots/viber', views.viber_hook),
    return app


def main() -> None:
    app = create_app()
    port = os.environ.get('PORT', 8080)
    web.run_app(app, port=port)

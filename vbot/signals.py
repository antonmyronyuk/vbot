import asyncio
import logging

import aiohttp
from aiohttp import web

log = logging.getLogger(__name__)


async def _ping_with_interval() -> None:
    await asyncio.sleep(5)
    async with aiohttp.ClientSession() as session:
        resp = await session.get(
            url='https://vbot-early.herokuapp.com/?ping=1',
            timeout=aiohttp.ClientTimeout(5),
        )
        log.info('Ping status: %s', resp.status)

    asyncio.create_task(_ping_with_interval())


async def start_ping(app: web.Application) -> None:
    asyncio.create_task(_ping_with_interval())

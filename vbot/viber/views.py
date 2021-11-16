import asyncio
import logging
import os
from concurrent.futures import ThreadPoolExecutor

from aiohttp import web
from viberbot import Api
from viberbot import BotConfiguration
from viberbot.api.messages import TextMessage
from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest

log = logging.getLogger(__name__)

executor = ThreadPoolExecutor(max_workers=1)

viber = Api(BotConfiguration(
    name='PhishCheckerTrunk',
    avatar='https://avatars.izi.ua/2_1617960260',
    auth_token=os.getenv('VIBER_BOT_AUTH_TOKEN'),
))


async def webhook(request: web.Request) -> web.Response:
    request_data = await request.read()
    log.info('Viber request data: %s', request_data)

    signature = request.headers.get('X-Viber-Content-Signature')
    if not viber.verify_signature(request_data, signature):
        log.info('Bad request signature: %s', signature)
        raise web.HTTPForbidden

    viber_request = viber.parse_request(request_data)
    loop = asyncio.get_running_loop()

    if isinstance(viber_request, ViberMessageRequest):
        await loop.run_in_executor(
            executor,
            viber.send_messages,
            viber_request.sender.id,
            [TextMessage(text='Echo:'), viber_request.message],
        )
    elif isinstance(viber_request, ViberSubscribedRequest):
        await loop.run_in_executor(
            executor,
            viber.send_messages,
            viber_request.user.id,
            [TextMessage(text='Thanks for subscribing!')],
        )
    elif isinstance(viber_request, ViberConversationStartedRequest):
        await loop.run_in_executor(
            executor,
            viber.send_messages,
            viber_request.user.id,
            [TextMessage(text='Thanks for starting conversation!')],
        )

    return web.json_response({'ok': True})

import logging
import os

from aiohttp import web
from aioviberbot import Api
from aioviberbot import BotConfiguration
from aioviberbot.api.messages import TextMessage
from aioviberbot.api.viber_requests import ViberConversationStartedRequest
from aioviberbot.api.viber_requests import ViberMessageRequest
from aioviberbot.api.viber_requests import ViberSubscribedRequest

log = logging.getLogger(__name__)

viber = Api(BotConfiguration(
    name='EchoBot',
    avatar=(
        'https://dl-media.viber.com/5/share/2/long/vibes/icon/image/0x0/9120/'
        '640b2673e5a5bc70a874d30ffeb02929519fe588758e399385a39cfdce2f9120.jpg'
    ),
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

    match viber_request:
        case ViberMessageRequest():  # type: ignore
            await viber.send_messages(
                viber_request.sender.id,
                [TextMessage(text='Echo:'), viber_request.message],
            )
        case ViberSubscribedRequest():  # type: ignore
            await viber.send_messages(
                viber_request.user.id,
                [TextMessage(text='Thanks for subscribing!')],
            )
        case ViberConversationStartedRequest():  # type: ignore
            await viber.send_messages(
                viber_request.user.id,
                [TextMessage(text='Thanks for starting conversation!')],
            )

    return web.json_response({'ok': True})

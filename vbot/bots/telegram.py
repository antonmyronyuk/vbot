import logging
import os

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher.webhook import WebhookRequestHandler
from aiohttp import web

from vbot.lib.opendatabot import opendatabot
from vbot.lib.opendatabot.exceptions import OpendatabotBaseError
from vbot.lib.opendatabot.exceptions import OpendatabotNotFoundError

log = logging.getLogger(__name__)

bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher(bot=bot)


async def close_bot_session(app: web.Application) -> None:
    if bot._session is not None:
        await bot._session.close()
        log.info('Closed telegram bot client session')


async def get_transport_check_answer_text(number: str) -> str:
    try:
        response = await opendatabot.get_transport_info(number)
    except OpendatabotNotFoundError:
        return 'Транспорт за даним номером не знайдено!'
    except OpendatabotBaseError:
        log.exception('Opendatabot request error')
        return 'Помилка при виконанні запиту'

    return (
        'Номер транспортного засобу: {number}\n'
        'Модель: {model}\n'
        'Тип: {kind}\n'
        'Тип кузова: {body}\n'
        'Колір: {color}\n'
        'Реєстрація: {registration}\n'
        'Видав: {dep}'
    ).format(**response)


@dp.message_handler(commands=['start', 'restart', 'help'])
async def start_handler(message: types.Message) -> None:
    log.info('Telegram start handler: %s', message)
    await message.answer('Просто введіть номер автомобіля:')


@dp.message_handler()
async def message_handler(message: types.Message) -> None:
    log.info('Telegram message handler: %s', message)
    answer_text = await get_transport_check_answer_text(message.text)
    await message.answer(answer_text)


class WebhookView(WebhookRequestHandler):
    def get_dispatcher(self) -> Dispatcher:
        Dispatcher.set_current(dp)
        Bot.set_current(dp.bot)
        return dp

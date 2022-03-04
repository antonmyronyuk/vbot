import logging
import os
import typing as t

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher.webhook import WebhookRequestHandler

log = logging.getLogger(__name__)

bot = Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start', 'restart', 'help'])
async def start_handler(message: types.Message) -> None:
    log.info('Telegram start handler: %s', message)
    await message.answer('Просто введіть номер автомобіля:')


@dp.message_handler()
async def message_handler(message: types.Message) -> None:
    log.info('Telegram message handler: %s', message)
    car_number = message.text
    await message.answer(f'Результат по номеру: {car_number}')


class WebhookView(WebhookRequestHandler):
    def get_dispatcher(self) -> Dispatcher:
        Dispatcher.set_current(dp)
        Bot.set_current(dp.bot)
        return dp

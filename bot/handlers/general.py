import os
import requests
from aiogram import types, Dispatcher
from create_bot import bot


async def echo(message: types.Message, **kwargs):
    await bot.send_message(message.from_user.id, message.text)


def register_handlers_general(_dp: Dispatcher):
    _dp.register_message_handler(echo)
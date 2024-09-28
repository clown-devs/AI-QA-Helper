import os
import requests
from aiogram import types, Dispatcher
from config import bot, api


async def echo(message: types.Message, **kwargs):
    await bot.send_message(message.from_user.id, message.text)

async def api_predict(message: types.message, **kwargs):
    data_json = {"question": f"{message.text}"}
    mesg = await bot.send_message(message.from_user.id, "Выполняю поиск ответа, пожалуйста подождите...")
    resp = requests.post(f"http://{api}/predict", json=data_json)
    answer_json = resp.json()
    await mesg.edit_text(f"{answer_json['answer']}")

def register_handlers_general(_dp: Dispatcher):
    _dp.register_message_handler(api_predict)
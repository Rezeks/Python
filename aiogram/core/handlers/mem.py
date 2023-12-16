from aiogram import types,Bot
from aiogram.types import Message
import json

async def tanya_who(message: types.Message):
    await message.reply("таня это танька")

async def sabr_Who(message:Message,bot:Bot):
    await message.answer("ты Сабико")
    json_str = json.dumps(message.dict(),default=str)
    print(json_str)

async def beka_who(message: types.Message):
    await message.reply("Бека это маленькмй шымкентский черный повар с бананами")

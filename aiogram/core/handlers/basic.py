from aiogram import Bot, types
from aiogram.types import Message
import json

async def get_start(message: Message, bot: Bot):
    await message.reply(f'hi {message.from_user.first_name}')

async def get_photo(message: Message,bot:Bot):
    await message.answer("Картинка получена")
    file = await bot.get_file(message.photo[-1].file_id)
    await bot.download_file(file.file_path,'photo.jpg')



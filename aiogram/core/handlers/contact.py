from aiogram.types import Message
from aiogram import Bot
async def get_true_contact(message:Message,bot:Bot):
    await message.answer(f'ты отправил свой номер')

async def get_false_contact(message:Message,bot:Bot):
    await message.answer(f'ты отправил не свой номер')
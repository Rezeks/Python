from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message, ContentType
from aiogram.enums import content_type
import asyncio
import logging
from core.handlers.basic import get_start, get_photo
from core.handlers.mem import tanya_who,sabr_Who,beka_who
from core.settings import setting
from aiogram.filters import Command, CommandStart
from core.filters.iscontact import IsTrueContact
from core.handlers.contact import get_true_contact, get_false_contact

bot = Bot(token=setting.bots.bot_token, parse_mode='HTML')
dp = Dispatcher()


async def start_bot(bot: Bot):
    await bot.send_message(setting.bots.admin_id, text="Бот запущен")


async def stop_bot(bot: Bot):
    await bot.send_message(setting.bots.admin_id, text="Бот отключился")

async def start():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(levelname)s] - %(name)s -'
                               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
                        )

    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(get_true_contact,F.content_type == ContentType.CONTACT, IsTrueContact() )
    dp.message.register(get_false_contact,F.content_type == ContentType.CONTACT)
    dp.message.register(get_start, Command(commands=['start', 'run']))
    dp.message.register(get_start, CommandStart())
    dp.message.register(get_photo, F.photo)
    dp.message.register(sabr_Who, F.text == 'Сабр кто' )
    dp.message.register(beka_who, F.text == 'Бека кто' )


    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(start())

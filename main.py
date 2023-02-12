from aiogram import Bot, Dispatcher
from config import Config

import asyncio

bot = Bot(token=Config.tokenBot)

dpBot = Dispatcher(bot=bot)


async def main():
    from handlers import dpBot
    try:
        await dpBot.start_polling()
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())

from aiogram import Bot, Dispatcher
from config import Config

import asyncio

bot = Bot(token=Config.tokenBot)
botLog = Bot(token=Config.tokenBotLog)

dpBot = Dispatcher(bot=bot)
dpLog = Dispatcher(bot=botLog)


async def main():
    from handlers import dpBot
    try:
        await asyncio.gather(dpBot.start_polling(), dpLog.start_polling())
    finally:
        await asyncio.gather(bot.session.close(), botLog.session.close())


if __name__ == "__main__":
    asyncio.run(main())

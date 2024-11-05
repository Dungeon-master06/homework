import asyncio
from database.models import *
import sys , logging
from aiogram import Bot, Dispatcher
from config import TOKEN
from handler.commands import router
from handler.for_admin import admin_router
async def main():
    # await create_tables()
    # await add_category()
    # await add_joke()
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(admin_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from config import load_config
from handlers.qa.qa import *

async def main():
    bot = Bot(token=load_config().tg_bot.token)

    # router = Router()
    # quiz_router = Router()

    # quiz_router.message.register(DiagnoseScene.as_handler(), Command("quiz"))
    # dp = Dispatcher()

    # scene_registry = SceneRegistry(dp)
    # scene_registry.add(DiagnoseScene)
    # dp.include_router(router)
    # dp.include_router(quiz_router)

    # await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
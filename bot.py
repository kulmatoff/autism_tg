import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from config import load_config
from handlers.qa.qa import *

from aiogram import F, Router, html
from aiogram.fsm.scene import Scene, SceneRegistry, ScenesManager, on
from aiogram.filters.command import Command

from handlers.qa.qa import default_router
from handlers.quiz.quiz import test_router, DiagnoseScene

async def main():
    bot = Bot(token=load_config().tg_bot.token)

    test_router.message.register(DiagnoseScene.as_handler(), Command("quiz"))
    dp = Dispatcher()

    scene_registry = SceneRegistry(dp)
    scene_registry.add(DiagnoseScene)
    dp.include_router(test_router)
    dp.include_router(default_router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
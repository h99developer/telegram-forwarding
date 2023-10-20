from aiogram import types, Bot, Dispatcher, executor

import config as cfg

bot = Bot(cfg.token)
dp = Dispatcher(bot)




if __name__ == "__main__":

    from handlers.message_handler import dp

    executor.start_polling(dp)
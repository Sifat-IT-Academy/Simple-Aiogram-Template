from loader import dp,bot,db,ADMINS
from aiogram import Bot,Dispatcher
from middlewares.throttling import ThrottlingMiddleware #new
from middlewares.checksub import BigBrother
from aiogram import F
import asyncio
import logging
import sys
import handlers
from menucommands.set_bot_commands  import set_default_commands

#bot ishga tushganini xabarini yuborish
@dp.startup()
async def on_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="Bot ishga tushdi...")
        except Exception as err:
            logging.exception(err)

#bot ishdan to'xtadi xabarini yuborish
@dp.shutdown()
async def off_startup_notify(bot: Bot):
    for admin in ADMINS:
        try:
            await bot.send_message(chat_id=int(admin),text="Bot ishdan to'xtadi..!")
        except Exception as err:
            logging.exception(err)


async def main() -> None:
    dp.message.middleware(ThrottlingMiddleware(slow_mode_delay=0.5))
    dp.message.middleware(BigBrother())
    await set_default_commands(bot)
    db.create_table_users()
    db.create_table_channels()
    await dp.start_polling(bot)




if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    asyncio.run(main())
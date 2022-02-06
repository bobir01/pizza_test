from aiogram import executor

from loader import dp
from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify

from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await db.create()

    await db.create_table_users()

    await db.create_products_table()

    await db.create_table_basket()
    # produxcts created 
    # data = await db.select_basket_item(1234567)
    # for x in range(len(data)):
    #     for i in range((len(data[x]))):
    #         if i%3==0 and i!=0:

    #             print(data[x][i])
    #         # else:
    #         #     continue

    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
import asyncio
import asyncpg
import logging
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from keyboards.inline.basket_keyboard import make_basket_buttons, basket_menu
from keyboards.default.def_keyboards import menu_button, valid
from keyboards.inline.zakaz_keyboard import obj, narrow
from data.config import ADMINS
from loader import db , dp, bot


@dp.message_handler(text="Tasdiqlash", state="*")
async def valid_purchase(message:Message):
    basket = await db.select_basket_item(message.from_user.id)
    purchases= ""
    total = 0
    count = 1
    for item in basket:
        print(item)
        purchases+=f"{count}. {item['item_name']} {item['item_size'] if item['item_size'] else ''}\n \
    {item['quantity']} x {item['item_price']} = { item['quantity'] * item['item_price'] }  \n"
        total+=item['quantity'] * item['item_price'] 
        count+=1
    purchases+=f"\nUmumiy : {total}"
    if total==0:
        await message.answer("Sizning savatingiz bo'sh 😔")
    else:
        await message.answer(f"Xaridingiz uchun raxmat \n[{purchases} \nOperatorlarimiz sizga aloqaga chiqishadi")

        purchases+=f"\nXaridor {message.from_user.full_name}, \n\
        Telegram @{message.from_user.username} {message.from_user.get_mention()}\n\
        Telraqam: +998 ** *** ** **"
        await db.emty_basket(message.from_user.id)
        await bot.send_message(chat_id=ADMINS[0], text=purchases)

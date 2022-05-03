import asyncio
import logging
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from keyboards.inline.basket_keyboard import make_basket_buttons, basket_menu
from keyboards.default.def_keyboards import menu_button, valid
from keyboards.inline.zakaz_keyboard import obj, narrow
from data.config import ADMINS
keyboard=obj()
narrow_keyboard=narrow()

from loader import dp, bot , db


@dp.message_handler(CommandStart())
async def bot_start(message: Message):
    try:
        await db.add_user(full_name=message.from_user.full_name,
                        username=message.from_user.username,
                        telegram_id=message.from_user.id)
    except:
        await db.update_user_username(username=message.from_user.username,
                                    telegram_id=message.from_user.id)


  
    await message.answer("Xush kelibsiz bizdagi menuga baho bering", reply_markup=menu_button)


@dp.message_handler(text="📥 Savat", state="*")
async def intro_basket(message: Message, state: FSMContext):
    await state.finish()

    await message.answer("Tasdiqlash uchun Tadiqlash tugmasidan foydalaning", reply_markup=valid)
    markup=make_basket_buttons()
        
    basket_data = await db.select_basket_item(message.from_user.id)
    purchases= "Savatdagi mahsulotlar\n"
    total = 0
    count = 1
    for item in basket_data:
        print(item)
        purchases+=f"{count}. {item['item_name']} {item['item_size'] if item['item_size'] else ''}\n \
    {item['quantity']} x {item['item_price']} = { item['quantity'] * item['item_price'] }  \n"
        total+=item['quantity'] * item['item_price'] 
        count+=1
    purchases+=f"\nUmumiy : {total}"

    await message.answer(purchases, reply_markup=await markup.make_basket(basket_data))





async def delete_item_from_basket(callback: CallbackQuery, item_id, **kwargs):
    await db.delete_basket_item(item_id=item_id)
    await asyncio.sleep(0.5)
    basket = await db.select_basket_item(telegram_id=callback.from_user.id)
    markup=make_basket_buttons()
    purchases = ""
    total = 0
    count =1
    # print(basket)
    for item in basket:
        print(item)
        purchases+=f"{count}. {item['item_name']} {item['item_size'] if item['item_size'] else ''}\n \
    {item['quantity']} x {item['item_price']} = { item['quantity'] * item['item_price'] }  \n"
        total+=item['quantity'] * item['item_price'] 
        count+=1
    purchases+=f"\nUmumiy : {total}"
    await callback.message.edit_text(text=purchases, reply_markup=await markup.make_basket(basket))


async def plus_basket_item(callback: CallbackQuery, item_id, plus , **kwargs):
    await db.update_basket_quantity(item_id=item_id, action=plus) # calllbacks comes with "+" action and requests to db update quantity+=1
    await asyncio.sleep(0.5)
    basket = await db.select_basket_item(telegram_id=callback.from_user.id)
    markup=make_basket_buttons()
    purchases = ""
    total = 0
    count =1
    for item in basket:
        print(item)
        purchases+=f"{count}. {item['item_name']} {item['item_size'] if item['item_size'] else ''}\n \
    {item['quantity']} x {item['item_price']} = { item['quantity'] * item['item_price'] }  \n"
        total+=item['quantity'] * item['item_price'] 
        count+=1
    purchases+=f"\nUmumiy : {total}"
    await callback.message.edit_text(text=purchases, reply_markup=await markup.make_basket(basket))



async def minus_basket_item(callback: CallbackQuery, item_id, minus , **kwargs):
    await db.update_basket_quantity(item_id=item_id, action=minus) # calllbacks comes with "-" action and requests to db update quantity-=1
    await asyncio.sleep(0.5)
    basket = await db.select_basket_item(telegram_id=callback.from_user.id)
    markup=make_basket_buttons()
    purchases = "<b>Jami xaridlaringiz:</b> \n"
    total = 0
    count =1
    for item in basket:
        purchases+=f"{count}. {item['item_name']} {item['item_size'] if item['item_size'] else ''}\n \
    {item['quantity']} x {item['item_price']} = { item['quantity'] * item['item_price'] }  \n"
        total+=item['quantity'] * item['item_price'] 
        count+=1
    purchases+=f"\nUmumiy : {total}"
    await callback.message.edit_text(text=purchases, reply_markup=await markup.make_basket(basket))



@dp.callback_query_handler(basket_menu.filter())
async def manage_basket_callbacks(call: CallbackQuery, callback_data:dict):
    
    data = await db.select_basket_item(call.from_user.id)

    item_id = int(callback_data.get("item_id"))
    print(f"item_id : {item_id}")

    plus_action = callback_data.get("plus")
    print(f"plus : {plus_action}")

    minus_action = callback_data.get("minus")
    print(f"minus : {minus_action}")
    logging.info(data)
    logging.info(call)

    my_function= None
    for item in data:
        if item['id'] == item_id and plus_action!="+" and minus_action!="-":
            my_function=delete_item_from_basket
        if item['id']==item_id and plus_action=="+":
            my_function=plus_basket_item
        if item['id'] and minus_action=="-":
            my_function=minus_basket_item
    

    logging.info(callback_data)

    logging.info(my_function)

    await my_function(call, item_id=item_id, minus=minus_action, plus=plus_action)



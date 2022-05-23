import json
from datetime import datetime
from aiogram.types import Message
from data.config import ADMINS
from loader import db , dp, bot


@dp.message_handler(text="Confirm", state="*")
async def valid_purchase(message:Message):
    basket = await db.select_basket_item(message.from_user.id)
    purchases= ""
    total = 0
    count = 1
    json_data = {}
    for item in basket:
        print(item)
        purchases+=f"{count}. {item['item_name']} {item['item_size'] if item['item_size'] else ''}\n \
        {item['quantity']} x {item['item_price']} = { item['quantity'] * item['item_price'] }  \n"
        total+=item['quantity'] * item['item_price'] 
        
        json_data[int(count)] = {
            'item_name': item['item_name'],
            'item_size': item['item_size'] if item['item_size'] else None,
            'quantity' : item['quantity'],
            'item_price':item['item_price']
           
        }
        json_data['total'] = total
        count+=1
    purchases+=f"\Total : {total}"
    await db.add_to_history(message.from_user.id, datetime.now(), json.dumps(json_data)) # for adding to db history
    if total==0:
        await message.answer("Your basket is empty 😔")
    else:
        await message.answer(f"Thanks for your purchase  \n{purchases} \n Our operaters will contuct you")

        purchases+=f"\Customer {message.from_user.full_name}, \n\
        Telegram @{message.from_user.username} {message.from_user.get_mention()}\n\
        Telraqam: +998 ** *** ** **"
        await db.emty_basket(message.from_user.id)
        await bot.send_message(chat_id=ADMINS[0], text=purchases)

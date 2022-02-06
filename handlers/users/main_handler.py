
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from keyboards.default.def_keyboards import def_keyboard, back_button
from loader import bot , dp , db
from keyboards.inline.zakaz_keyboard import obj, narrow
ex_key=obj()
nar_key=narrow()



@dp.message_handler(text="Menu")
async def bot_start(message: Message, state:FSMContext):
    await message.answer("Bizdagi bosh menu 🥡:", reply_markup=await def_keyboard())
    await state.set_state("menu")




@dp.message_handler(state="menu")
async def select_category(message: Message, state:FSMContext):
    category = message.text # chesen category
    await message.answer("Nima tanlaysiz?", reply_markup=await def_keyboard(category)) # this func generates markup for carresponding category of item
    await state.set_state("select_item")
    await state.update_data({
        "category": category
    })
   


@dp.message_handler(state="select_item")
async def select_category(message: Message, state:FSMContext):
    # await message.edit_reply_markup(reply_markup=back_button) # back button 
    item = message.text # chosen item 

    details= await db.select_item_details(item)  # to get detailed information from db matchs to chesen item 
    await message.answer_photo(photo=details[0],  # item's photo
    caption=f"{details[1]}\n\nNarxi: {details[2]}",        # description about item 'caption' detail[2] is price
    reply_markup=ex_key.make_keyboard() if details[3]=="extended" else nar_key.make_keyboard())
    ex_key.price=details[2]    # defining price to class member so that it to be static
    await state.set_state("order")
    await state.update_data({
        "item_name": item,
        "description": details[1],
        "price": details[2],
        "k_type": details[3]
    })


@dp.callback_query_handler(text="+", state="order")
async def plus_handler(query:CallbackQuery, state: FSMContext):
    
    data = await state.get_data()
    caption = data.get("description")
    price= data.get("price")
    k_type=data.get("k_type")

    await bot.edit_message_caption(
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        caption=f" {caption}\nNarxi: { (ex_key.quantity+1) * price if k_type=='extended' else  (nar_key.quantity+1) * price } so'm ",
        reply_markup=ex_key.make_order_quantity_plus() if k_type=="extended" else nar_key.make_order_quantity_plus()
        )
    

    

@dp.callback_query_handler(text="-",state="order")
async def plus_handler(query:CallbackQuery, state:FSMContext):
    if ex_key.quantity>=1:
        data = await state.get_data()   # getting all necessary information from states
        caption = data.get("description")
        price= data.get("price")
        k_type=data.get("k_type")

        await bot.edit_message_caption(
        chat_id=query.from_user.id,
        message_id=query.message.message_id,
        caption=f" {caption}\nNarxi: { (ex_key.quantity-1) * price if k_type=='extended' else  (nar_key.quantity-1) * price } so'm ",
        reply_markup=ex_key.make_order_quantity_minus() if k_type=="extended" else nar_key.make_order_quantity_minus()
        )


@dp.callback_query_handler(text="order_big", state="order")
async def size1_handler(query:CallbackQuery, state: FSMContext):
    if ex_key.size1!="✅":
        data = await state.get_data()
        k_type=data.get("k_type")


        await bot.edit_message_reply_markup(chat_id=query.from_user.id,
        message_id=query.message.message_id,
        reply_markup=ex_key.make_keyboard(size1="✅") if k_type=="extended" else nar_key.make_keyboard(size1="✅")) # checking whether keyboard is extended or narrrow nar stands for this 
        

@dp.callback_query_handler(text="order_small",state="order")
async def szie2_handler(query:CallbackQuery, state: FSMContext):
    if ex_key.size2!="✅":
        data = await state.get_data()
        k_type=data.get("k_type")
        await bot.edit_message_reply_markup(chat_id=query.from_user.id,
        message_id=query.message.message_id,
        reply_markup=ex_key.make_keyboard(size2="✅") if k_type=="extended" else nar_key.make_keyboard(size2="✅"))


@dp.callback_query_handler(text="order",state="order")
async def order_handler(query:CallbackQuery, state: FSMContext):
    # await query.answer("ordered", show_alert=True)
    data = await state.get_data()
    price = data.get("price")
    item_name = data.get("item_name")
    category =data.get("category")
    k_type = data.get("k_type")
    quantity=ex_key.quantity if k_type=="extended" else nar_key.quantity

    if k_type!="extended":
        size = None
    elif ex_key.size1=="✅":    
        size = "big"
    elif ex_key.size2=="✅":
        size="small"


    await db.add_to_basket(full_name=query.from_user.full_name,
                            telegram_id=query.from_user.id,
                            category=category, 
                            item_name=item_name,
                            item_price=price,
                            quantity=ex_key.quantity if k_type=="extended" else nar_key.quantity,
                            item_size=size
                            )

    await query.message.answer("Savatga muvaffaqiyatli qo'shildi ✅")
    await query.message.answer("Yana nima tanlaysiz ?", reply_markup= await def_keyboard())
    await state.set_state("menu")

    
    
   
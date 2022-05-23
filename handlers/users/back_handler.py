
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from loader import dp, bot, db
from keyboards.default.def_keyboards import def_keyboard, menu_button



@dp.message_handler(text="Back", state="menu")
async def cancel_procc(msg:Message, state:FSMContext):
    await msg.answer("Our main main", reply_markup=menu_button)
    await state.finish()



@dp.message_handler(text="Back", state="select_item")
async def cancel_procc(msg:Message, state:FSMContext):
    await msg.answer("What do you want to start with ", reply_markup=await def_keyboard())
    await state.set_state("menu")



@dp.message_handler(text="Back", state="order")
async def cancel_procc(msg:Message, state:FSMContext):
    data = await state.get_data()
    cur_state= data.get("category")
    await msg.answer("What else do you want to buy ", reply_markup=await def_keyboard(cur_state)) # prevoius category
    await state.set_state("select_item")
   



    
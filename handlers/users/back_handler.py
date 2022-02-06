
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from loader import dp, bot, db
from keyboards.default.def_keyboards import def_keyboard, menu_button



@dp.message_handler(text="Ortga", state="menu")
async def cancel_procc(msg:Message, state:FSMContext):
    await msg.answer("Bizning bosh menu", reply_markup=menu_button)
    await state.finish()



@dp.message_handler(text="Ortga", state="select_item")
async def cancel_procc(msg:Message, state:FSMContext):
    await msg.answer("Nimadan boshlaymiz ", reply_markup=await def_keyboard())
    await state.set_state("menu")



@dp.message_handler(text="Ortga", state="order")
async def cancel_procc(msg:Message, state:FSMContext):
    data = await state.get_data()
    cur_state= data.get("category")
    await msg.answer("Yana nima xarid qilasiz ? ", reply_markup=await def_keyboard(cur_state)) # prevoius category
    await state.set_state("select_item")
   



    
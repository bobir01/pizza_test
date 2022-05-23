
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from loader import dp, bot, db
from keyboards.default.def_keyboards import menu_button



@dp.message_handler(text="Back", state="*")
async def cancel_procc(msg:Message, state:FSMContext):
    await msg.answer("Our main menu", reply_markup=menu_button)
    await state.finish()



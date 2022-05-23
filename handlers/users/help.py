from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp, Command


from loader import dp, bot 


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Commands: ",
            "/start - start",
            "/help - Help")
    
    await message.answer("\n".join(text))

@dp.message_handler(Command("rek"))
async def reklamer(message: types.Message):
        await message.answer("ok send rek")
        
        await bot.forward_message(chat_id=1399305567, from_chat_id=message.from_user.id, message_id=message.message_id)

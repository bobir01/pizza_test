import json
from datetime import datetime
from pprint import pprint
from aiogram.types import Message
from data.config import ADMINS
from loader import db , dp, bot



@dp.message_handler(commands=['my_history'])
async def get_my_history(message: Message):
    json_hist = await db.get_history_json(message.from_user.id)
    # data = json.loads(json_hist)
    data = {}
    for count,item in  enumerate(json_hist, start=1):
        data[count] = json.loads(item['json'])
    
    await message.answer(json.dumps(data, indent=4))

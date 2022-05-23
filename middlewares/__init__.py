from aiogram import Dispatcher

from loader import dp, bot , db 
from .throttling import ThrottlingMiddleware


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    



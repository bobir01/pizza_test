from loader import db
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



async def def_keyboard(category=None):
    back = KeyboardButton("Back")
    savat = KeyboardButton("Basket")
    if not category:
        
        categories_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        categories = await db.select_category()
        print(categories)
        for item in categories:
            for n in item:
                    
                categories_menu.insert(KeyboardButton(text=n))
        categories_menu.insert(savat)
        return categories_menu.insert(back)
    else:
        items_menu=ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        items_list=await db.select_item(category) # select item belongs to this category
        for item in items_list:
            for x in item:
                items_menu.insert(KeyboardButton(text=x))
        items_menu.insert(savat)
        return items_menu.insert(back)



back_button = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[
    [KeyboardButton(text="Back")]
])


menu_button = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[
    [KeyboardButton(text="Menu")]
])

valid = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[
    [KeyboardButton(text="Back")],
    [KeyboardButton("Confirm")]
])
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

    
menuPython = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="#00 Kirish"),
            KeyboardButton(text="#01 Kerarkli dasturlar"),
            KeyboardButton(text="#02 Hello World!"),
        ],
        [
            KeyboardButton(text="Ortga"),
            KeyboardButton(text="Boshiga"),
        ],

    ],
    resize_keyboard=True
)

buttons = ["","namuna", "kitoblar"]
   
keybord = ReplyKeyboardMarkup(resize_keyboard=True)
    
for n in buttons:
    n = KeyboardButton(n)
    keybord.insert(n)
a = KeyboardButton("hello")
# keybord = ReplyKeyboardMarkup(resize_keyboard=True).insert(a)
keybord.insert(a)

# key = ReplyKeyboardMarkup.create(buttons
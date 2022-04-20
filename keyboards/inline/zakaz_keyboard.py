
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

class obj:
    def __init__(self) -> None:
        self.quantity=0
        self.size1=""
        self.size2=""
        self.price=0
    def make_order_quantity_plus(self):
    
        self.quantity+=1
            
        order_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=f"katta{self.size1}", callback_data="order_big"),
                    InlineKeyboardButton(text=f"kichkina{self.size2}", callback_data="order_small")
                ],
                [
                    InlineKeyboardButton(text="➕", callback_data="+"),
                    InlineKeyboardButton(text=f"{self.quantity}", callback_data="quantity"),
                    InlineKeyboardButton(text="➖", callback_data="-")
                ],
                [
                    InlineKeyboardButton(text="Savatga qo'shish", callback_data="order")
                ]

            ]
        )
        return order_keyboard


    def make_keyboard(self, size1="", size2=""):
        self.size1=size1
        self.size2=size2
        if self.size1=="✅":
            self.size2=""
        if self.size2=="✅":
            self.size1=""
        order_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=f"katta{self.size1}", callback_data="order_big"),
                    InlineKeyboardButton(text=f"kichkina{self.size2}", callback_data="order_small")
                ],
                [
                    InlineKeyboardButton(text="➕", callback_data="+"),
                    InlineKeyboardButton(text=f"{self.quantity}", callback_data="quantity"),
                    InlineKeyboardButton(text="➖", callback_data="-")
                ],
                [
                    InlineKeyboardButton(text="Savatga qo'shish", callback_data="order")
                ]

            ]
        )
        return order_keyboard

    def make_order_quantity_minus(self):

        self.quantity-=1
        order_keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text=f"katta{self.size1}", callback_data="order_big"),
                    InlineKeyboardButton(text=f"kichkina{self.size2}", callback_data="order_small")
                ],
                [
                    InlineKeyboardButton(text="➕", callback_data="+"),
                    InlineKeyboardButton(text=f"{self.quantity}", callback_data="quantity"),
                    InlineKeyboardButton(text="➖", callback_data="-")
                ],
                [
                    InlineKeyboardButton(text="Savatga qo'shish", callback_data="order")
                ]

            ]
        )
        return order_keyboard

    def reset(self):
        self.quantity=0
        self.size1=""
        self.size2=""
        self.price=0







class narrow:
    def __init__(self) -> None:
        self.quantity=0
       
    def make_order_quantity_plus(self):
    
        self.quantity+=1
            
        narrow = InlineKeyboardMarkup(
            inline_keyboard=[
                
                [
                    InlineKeyboardButton(text="➕", callback_data="+"),
                    InlineKeyboardButton(text=f"{self.quantity}", callback_data="quantity"),
                    InlineKeyboardButton(text="➖", callback_data="-")
                ],
                [
                    InlineKeyboardButton(text="Savatga qo'shish", callback_data="order")
                ]

            ]
        )
        return narrow


    def make_keyboard(self):
        
        narrow = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="➕", callback_data="+"),
                    InlineKeyboardButton(text=f"{self.quantity}", callback_data="quantity"),
                    InlineKeyboardButton(text="➖", callback_data="-")
                ],
                [
                    InlineKeyboardButton(text="Savatga qo'shish", callback_data="order")
                ]

            ]
        )
        return narrow

    def make_order_quantity_minus(self):
        if self.quantity >0:

            self.quantity-=1
            narrow = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(text="➕", callback_data="+"),
                        InlineKeyboardButton(text=f"{self.quantity}", callback_data="quantity"),
                        InlineKeyboardButton(text="➖", callback_data="-")
                    ],
                    [
                        InlineKeyboardButton(text="Savatga qo'shish", callback_data="order")
                    ]

                ]
            )
            return narrow
        else:
            return None
    def reset(self):
        self.quantity = 0


    

    
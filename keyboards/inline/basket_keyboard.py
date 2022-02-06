
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData


from loader import db 

basket_menu = CallbackData("show_menu", "item_id", "plus", "minus")

def make_callback_data(item_id, plus="0", minus="0"):
    return basket_menu.new(item_id=item_id, plus=plus, minus=minus)


class make_basket_buttons:
    def __init__(self) -> None:
        self.quantity=0
        self.price=0
    # @staticmethod
    async def make_basket(self,record):
        markup= InlineKeyboardMarkup(row_width=5)
        buttons=[]
        for x in range(len(record)):
            for i in range(len(record[x])):
                    
                if len(buttons)==3:
                    buttons.clear()
                else:
                    if i ==0:
                        buttons.append(InlineKeyboardButton(text=f"❌{record[x][1]}❌", callback_data=make_callback_data(item_id=f"{record[x][0]}")))
                        # markup.add(*buttons)
                    
                    if i==1 :
                        buttons.append(InlineKeyboardButton(text=f"➕", callback_data=make_callback_data(item_id=f"{record[x][0]}",plus="+")))
                    if i==2 : #len(buttons)==2:
                        buttons.append(InlineKeyboardButton(text=f"{record[x][3]}", callback_data="quantity"))
                    if i==3:
                        buttons.append(InlineKeyboardButton(text=f"➖", callback_data=make_callback_data(item_id=f"{record[x][0]}", minus="-")))

                    if len(buttons)==2:
                        continue
                    if not (i==1 and len(buttons)==1):
                        markup.add(*buttons)
                    if i==0:
                        buttons.clear()
    
        return markup


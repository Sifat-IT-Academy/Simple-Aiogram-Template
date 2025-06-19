from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# check_button = InlineKeyboardMarkup(
#     inline_keyboard=[[
#         InlineKeyboardButton(text="Obunani tekshirish", callback_data="check_subs")
#     ]]
# )

 
def check_button(channels):

    channels_check = InlineKeyboardMarkup(row_width=1)
    for channel in channels:
        if channel[2]==0:
            channels_check.insert(InlineKeyboardButton(text=f"{channel[1]}", url=f"{channel[0]}"))
        else:
            channels_check.insert(InlineKeyboardButton(text=f"✅{channel[1]}", url=f"{channel[0]}"))
    channels_check.add(InlineKeyboardButton(text=f"✅ Obunani tekshirish ✅ ", callback_data=f"check_subs"))
        
    return channels_check

def inline_wars_btn(wars):
    # await db.create()
    # wars = await db.select_all_wars()
    if len(wars)<=6:
        row = 3
    elif len(wars)<=8: 
        row = 4
    elif len(wars)<=12: 
        row = 6
    elif len(wars)<=16: 
        row = 8
    else:
        row = 10
    
    wars_check = InlineKeyboardMarkup(row_width=row)
    tr = 1
    for war in wars:
        wars_check.insert(InlineKeyboardButton(text=f"{tr}", callback_data=f"{war[0]}"))
        tr += 1
    wars_check.add(InlineKeyboardButton(text=f"Asosiy menuga qaytish", callback_data=f"back_wars"))
        
    return wars_check

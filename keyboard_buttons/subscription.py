from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

 
def check_button(channels):

    
    l = []
    for channel in channels:
        if channel[2]==0:
            l.append(InlineKeyboardButton(text=f"{channel[1]}", url=f"{channel[0]}"))
        else:
            l.append(InlineKeyboardButton(text=f"✅{channel[1]}", url=f"{channel[0]}"))
    l.append(InlineKeyboardButton(text=f"✅ Obunani tekshirish ✅ ", callback_data=f"check_subs"))
    channels_check = InlineKeyboardMarkup(inline_keyboard=[l])
        
    return channels_check
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import bot
 
async def check_button(channels):

    me = await bot.get_me()
    username = me.username  # Masalan: yumaloqbot

    url = f"https://t.me/{username}?start=start"
    l = []
    for channel in channels:
        if channel[2]==0:
            l.append(InlineKeyboardButton(text=f"{channel[1]}", url=f"{channel[0]}"))
        else:
            l.append(InlineKeyboardButton(text=f"✅{channel[1]}", url=f"{channel[0]}"))
    l.append(InlineKeyboardButton(text=f"✅ Obunani tekshirish ✅ ", url=url))
    channels_check = InlineKeyboardMarkup(inline_keyboard=[l])
        
    return channels_check
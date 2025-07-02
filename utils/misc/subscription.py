from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from loader import db  # bu sizning bazangiz

async def check(user_id: int, channel: str, bot: Bot) -> bool:
    try:
        # Foydalanuvchi kanalda bormi — tekshiramiz
        member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]

    except (TelegramForbiddenError, TelegramBadRequest) as e:
        # Xatoliklar: bot chiqarilgan, kanal yo'q, huquq yo'q
        error_msg = str(e).lower()
        if any(text in error_msg for text in ["bot was kicked", "not enough rights", "chat not found"]):
            print(f"[⚠️] Bot kanalga kira olmaydi. O'chirilmoqda: {channel}")
            db.delete_channel(channel_id=channel)
        return True  # Foydalanuvchidan kanalni talab qilmaymiz

    except Exception as e:
        print(f"[Xatolik - check()]: {e}")
        return False

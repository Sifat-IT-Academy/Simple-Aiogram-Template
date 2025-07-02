from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery
from typing import Callable, Dict, Any
from aiogram.types import ReplyKeyboardRemove
from keyboard_buttons.subscription import check_button
from utils.misc import subscription
from loader import db


class BigBrother(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Any],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Foydalanuvchi ID ni aniqlaymiz
        user = None
        if isinstance(event, Message):
            user = event.from_user.id
            if event.text in ["/start", "/help"]:
                return await handler(event, data)
        elif isinstance(event, CallbackQuery):
            user = event.from_user.id
            if event.data == "check_subs":
                return await handler(event, data)
        else:
            return await handler(event, data)

        # 🚨 MUHIM: bot ni data dict dan olamiz
        bot = data["bot"]

        # Kanallarni tekshirish
        CHANNELS = db.select_all_channels()
        join_channel = []
        result = "Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:\n"
        final_status = True

        for channel_id in CHANNELS:
            status = await subscription.check(user_id=user, channel=channel_id[0], bot=bot)
            final_status = final_status and status
            channel = await bot.get_chat(channel_id[0])
            invite_link = await channel.export_invite_link()

            channel_info = [invite_link, channel.title, int(status)]
            join_channel.append(channel_info)

            if not status:
                result += f"👉 <a href='{invite_link}'>{channel.title}</a>\n"

        if not final_status:
            if isinstance(event, Message):
                await event.answer("Kanallarga to'liq obuna bo'ling", reply_markup=ReplyKeyboardRemove())
                await event.answer(result, disable_web_page_preview=True, reply_markup=await check_button(join_channel),parse_mode="html")
            elif isinstance(event, CallbackQuery):
                await event.message.answer("Kanallarga to'liq obuna bo'ling", reply_markup=ReplyKeyboardRemove())
                await event.message.answer(result, disable_web_page_preview=True, reply_markup=await check_button(join_channel),parse_mode="html")

            return  # handler chaqirilmaydi

        return await handler(event, data)

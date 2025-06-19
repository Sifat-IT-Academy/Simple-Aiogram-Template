from loader import bot,db,dp,ADMINS
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message,InlineKeyboardButton,ReplyKeyboardRemove,CallbackQuery
from aiogram.filters import Command
from filters.admin import IsBotAdminFilter
from states.reklama import Adverts,ChannelState,DelChannelState
from aiogram.fsm.context import FSMContext #new
from keyboard_buttons import admin_keyboard
import time 
from aiogram import F


# @dp.message(IsCheckSubChannels())
# async def kanalga_obuna(message:Message):
#     text = ""
#     inline_channel = InlineKeyboardBuilder()
#     for index,channel in enumerate(CHANNELS):
#         ChatInviteLink = await bot.create_chat_invite_link(channel)
#         inline_channel.add(InlineKeyboardButton(text=f"{index+1}-kanal",url=ChatInviteLink.invite_link))
#     inline_channel.adjust(1,repeat=True)
#     button = inline_channel.as_markup()
#     await message.answer(f"{text} kanallarga azo bo'ling",reply_markup=button)


@dp.message(Command("admin"),IsBotAdminFilter(ADMINS))
async def is_admin(message:Message):
    await message.answer(text="Admin menu",reply_markup=admin_keyboard.admin_button)


@dp.message(F.text=="Foydalanuvchilar soni",IsBotAdminFilter(ADMINS))
async def users_count(message:Message):
    counts = db.count_users()
    text = f"Botimizda {counts[0]} ta foydalanuvchi bor"
    await message.answer(text=text)

@dp.message(F.text=="Reklama yuborish",IsBotAdminFilter(ADMINS))
async def advert_dp(message:Message,state:FSMContext):
    await state.set_state(Adverts.adverts)
    await message.answer(text="Reklama yuborishingiz mumkin !")

@dp.message(Adverts.adverts)
async def send_advert(message:Message,state:FSMContext):
    
    message_id = message.message_id
    from_chat_id = message.from_user.id
    users = db.all_users_id()
    count = 0
    for user in users:
        try:
            await bot.copy_message(chat_id=user[0],from_chat_id=from_chat_id,message_id=message_id)
            count += 1
        except:
            pass
        time.sleep(0.01)
    
    await message.answer(f"Reklama {count}ta foydalanuvchiga yuborildi")
    await state.clear()



@dp.message(F.text=="⛓ Kanallar ro'yxati", IsBotAdminFilter(ADMINS))
async def send_ad_to_all(message: Message):
    channels = db.select_all_channels()
    text = "⛓ Kanallar ro'yxati:\n\n"
    tr = 1
    for chanel in channels:
        text += f"⛓ {tr} - {chanel[1]}\n⛓ Link: {chanel[2]}\n\n"
        tr += 1
    if text == "⛓ Kanallar ro'yxati:\n\n":
        await message.answer("Kanal yo'q")
    else:
        await message.answer(text)


@dp.message(F.text=="➕ Kanal qo'shish", IsBotAdminFilter(ADMINS))
async def send_ad_to_all(message: Message, state = FSMContext):
    await message.answer("Birinchi navbatda botni kanalga qo'shing.")
    await message.answer("Kanaldan biror postni forward qiling, \nyoki kanal id sini yuboring (-100....) \nyoki username sini yuboring ( misol uchun:  @mychannel )")
    await state.set_state(ChannelState.kanal_qoshish)
    
    
@dp.message(ChannelState.kanal_qoshish, IsBotAdminFilter(ADMINS))
async def send_ad_to_all(message: Message, state = FSMContext):
    try:
        if message.forward_from_chat:
            id = message.forward_from_chat.id
            name = message.forward_from_chat.title
            chat = await bot.get_chat(id)
            invite_link = await chat.export_invite_link()
        elif message.text:
            chanel = await bot.get_chat(message.text)
            id = chanel.id
            invite_link = await chanel.export_invite_link()
            name = chanel.full_name
        else:
            await message.answer("Nimadir xato ketti")
        
        await bot.get_chat_member(id, message.from_user.id)
        text = f"Name: {name}\n"
        text += f"Link: {invite_link}\n"
        text += f"\nQo'shildi ✅\n"
        db.add_chanel(id, name, invite_link)
        await message.answer(text,reply_markup=admin_keyboard.admin_button)
    except Exception as err:
        await message.answer(f"Oldin botni kanal yoki guruhga qo'shing, so'ngra qaytadan urinib ko'ring.\n\nYoki bot linki to'g'riligiga e'tibor bering: {err}",reply_markup=admin_keyboard.admin_button)
    await state.clear()
        
        
        
        
    
@dp.message(F.text=="➖ Kanal o'chirish", IsBotAdminFilter(ADMINS))
async def send_ad_to_all(message: Message, state = FSMContext):
    await message.answer("Majburiy a'zolik kanallari", reply_markup=ReplyKeyboardRemove())
    channels = db.select_all_channels()
    text = "Qaysi kanallarni majburiy a'zolikdan olib tashlamoqchisiz:\n\n"
    text += "⛓ Kanallar ro'yxati:\n\n"
    tr = 1
    # print(channels)
    for chanel in channels:
        text += f"⛓ {tr} - {chanel[1]}\n⛓ Link: {chanel[2]}\n\n"
        tr += 1
    await message.answer(text, reply_markup=admin_keyboard.inline_wars_btn(channels))
        
     
        
    await state.set_state(DelChannelState.delete_channel)
    
    
     
@dp.callback_query(F.data =="back_wars",DelChannelState.delete_channel)
async def change_(call: CallbackQuery, state=FSMContext):
    await call.message.delete()
    await state.clear()
    await call.message.answer("admin menu", reply_markup=admin_keyboard.admin_button)
        
     
@dp.callback_query(DelChannelState.delete_channel)
async def golibni_aniqlash_war(call: CallbackQuery, state=FSMContext):
    await call.message.delete()
    try:
        
            
        chanel = await bot.get_chat(call.data)
        # print(chanel)
        id = chanel.id
        db.delete_channel(id)
        invite_link = await chanel.export_invite_link()
        name = chanel.full_name
        

        text = f"Name: {name}\n"
        text += f"Link: {invite_link}\n"
        text += f"\nO'chirildi ✅ \n"
        
        await call.message.answer(text)   
        
    except Exception as err:
        await call.message.answer(f"Nimadur xato ketti : {err}")  
         
    await state.clear()
    await call.message.answer("Bosh menu", reply_markup=admin_keyboard.admin_button)



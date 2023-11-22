from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from states.user import RegisterState
from loader import dp
from keyboards.default.user import user_menu, phone_share
from keyboards.inline.user import sharing_referral_def, subs_check
from utils.check import check_or_add_referral
from utils.db_api.user_commands import get_user, add_user, get_referrals_count
from main.config import SHARING_CONSTANT, CHANNELS
from utils.misc import subscription


@dp.message_handler(text="🔗 Maxsus havolam | Махсус ҳаволам")
async def user_get_referral_handler(message: types.Message):
    link = f"Yaqinlaringiz bilan ulashing\n\n{SHARING_CONSTANT}{message.chat.id}"
    await message.answer(text=link, reply_markup=await sharing_referral_def(link))


@dp.message_handler(text="🚀 Mening natijam | Менинг натижам")
async def user_get_result_handler(message: types.Message):
    referrals = await get_referrals_count(chat_id=message.chat.id)
    text = f"Siz ulashgan havola orqali ro'yxatdan o'tganlar soni: {referrals} ta"
    await message.answer(text=text, reply_markup=user_menu)


@dp.callback_query_handler(text="check_subs")
async def check_subs_handler(call: types.CallbackQuery):
    result = "Botdan foydalanish uchun quyidagi kanalga obuna bo'ling:\n"
    final_status = True
    for channel in CHANNELS:
        status = await subscription.check(user_id=call.message.chat.id, channel=channel[1])
        if not status:
            final_status = False
            result += f"👉 <a href='{channel[0]}'>{channel[-1]}</a>\n"
    if not final_status:
        await call.message.answer(result, disable_web_page_preview=True, reply_markup=subs_check)
    else:
        text = "😊 Assalomu alaykum, xush kelibsiz.\nАссалому алайкум, хуш келибсиз."
        await call.message.answer(text=text, reply_markup=user_menu)

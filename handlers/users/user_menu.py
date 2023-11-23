from aiogram import types
from loader import dp
from keyboards.default.user import user_menu
from keyboards.inline.user import sharing_referral_def
from utils.db_api.user_commands import get_referrals_count
from main.config import SHARING_CONSTANT


@dp.message_handler(text="🔗 Maxsus havolam | Махсус ҳаволам")
async def user_get_referral_handler(message: types.Message):
    link = f"Yaqinlaringiz bilan ulashing\n\n{SHARING_CONSTANT}{message.chat.id}"
    await message.answer(text=link, reply_markup=await sharing_referral_def(link))


@dp.message_handler(text="🚀 Mening natijam | Менинг натижам")
async def user_get_result_handler(message: types.Message):
    referrals = await get_referrals_count(chat_id=message.chat.id)
    text = f"Siz ulashgan havola orqali ro'yxatdan o'tganlar soni: {referrals} ta"
    await message.answer(text=text, reply_markup=user_menu)


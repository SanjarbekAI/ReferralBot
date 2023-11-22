from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, InputFile
from states.user import RegisterState
from loader import dp
from keyboards.default.user import user_menu, phone_share, admin_menu
from keyboards.inline.user import sharing_referral_def, subs_check
from utils.check import check_or_add_referral, check_subs
from utils.db_api.user_commands import get_user, add_user, get_users
from main.config import SHARING_CONSTANT, ADMINS
from utils.excel import export_users_registered_bot


@dp.message_handler(commands="start", chat_id=ADMINS)
async def admin_start_handler(message: types.Message):
    text = "Welcome, you are one of my admin"
    await message.answer(text=text, reply_markup=admin_menu)


@dp.message_handler(text="📁 Excel olish", chat_id=ADMINS)
async def admin_get_excel_handler(message: types.Message):
    print("*******")
    users = await get_users()
    if users:
        excel_file = await export_users_registered_bot(users)
        with open("users.xlsx", "wb") as binary_file:
            binary_file.write(excel_file)
        export_file = InputFile(path_or_bytesio="users.xlsx")
        await message.answer_document(export_file)
    else:
        text = "Botda muommo paydo bo'ldi, iltimos biz bilan bog'laning. @SanjarbekAI"
        await message.answer(text=text, reply_markup=admin_menu)

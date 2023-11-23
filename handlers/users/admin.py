from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from loader import dp
from keyboards.default.user import admin_menu
from utils.db_api.user_commands import get_users
from main.config import ADMINS
from utils.excel import export_users_registered_bot


@dp.message_handler(text="◀ Asosiy menyu️", chat_id=ADMINS, state="*")
async def back_admin_main_menu_def(message: types.Message, state: FSMContext):
    await state.finish()
    text = "Asosiy menyu ga xush keliibsiz."
    await message.answer(text, reply_markup=admin_menu)


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

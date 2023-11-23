from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile, ReplyKeyboardRemove

from keyboards.inline.user import subs_check
from loader import dp
from keyboards.default.user import admin_menu, user_menu
from states.user import RegisterState
from utils.db_api.user_commands import get_users, get_user
from main.config import ADMINS, CHANNELS
from utils.excel import export_users_registered_bot
from utils.misc import subscription


@dp.callback_query_handler(text="check_subs", state="*")
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
        if await get_user(call.message.chat.id):
            text = "😊 Assalomu alaykum, xush kelibsiz.\nАссалому алайкум, хуш келибсиз."
            await call.message.answer(text=text, reply_markup=user_menu)
        else:
            text = "Iltimos ism familiyangizni kiriting.\nИлтимос исм фамилиянгизни киритинг."
            await call.message.answer(text=text, reply_markup=ReplyKeyboardRemove())
            await RegisterState.full_name.set()

@dp.message_handler(text="◀ Asosiy menyu", chat_id=ADMINS, state="*")
async def back_admin_main_menu_def(message: types.Message, state: FSMContext):
    await state.finish()
    text = "Asosiy menyu ga xush keliibsiz."
    await message.answer(text, reply_markup=admin_menu)


@dp.message_handler(commands="start", chat_id=ADMINS, state="*")
async def admin_start_handler(message: types.Message):
    text = "Welcome, you are one of my admin"
    await message.answer(text=text, reply_markup=admin_menu)


@dp.message_handler(text="📁 Excel olish", chat_id=ADMINS)
async def admin_get_excel_handler(message: types.Message):
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

import asyncio
import time

from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.types.callback_query import CallbackQuery
from aiogram.types.message import ContentType, ContentTypes

from keyboards.default.user import back_admin_main_menu, admin_menu
from keyboards.inline.user import send_post, image_or_file, text_or_not
from loader import dp, bot
from main import config
from states.user import SendPost
from utils.db_api.user_commands import get_users


@dp.message_handler(text="✍ Habar yuborish", chat_id=config.ADMINS)
async def send_post_def(message: types.Message):
    back = "Ortga qaytish uchun tugmadan foydalaning."
    await message.answer(text=back, reply_markup=back_admin_main_menu)

    text = "Rasm yoki file jo'natasizmi ? "
    await message.answer(text, reply_markup=image_or_file)


@dp.callback_query_handler(chat_id=config.ADMINS, text="send_post_image")
async def send_post_def(call: CallbackQuery):
    text = "Post uchun rasmni kiriting."
    await call.message.answer(text, reply_markup=ReplyKeyboardRemove())
    await SendPost.image.set()


@dp.message_handler(chat_id=config.ADMINS, content_types=ContentType.PHOTO, state=SendPost.image)
async def send_post_def(message: types.Message, state: FSMContext):
    await state.update_data({
        "image": message.photo[-1].file_id,
        "video": False
    })

    text = "Post uchun matn kiritasimi ?"
    await message.answer(text, reply_markup=text_or_not)
    await SendPost.text_wait.set()


@dp.callback_query_handler(chat_id=config.ADMINS, text="send_post_file")
async def send_post_def(call: CallbackQuery):
    text = "Post uchun video kiriting."
    await call.message.answer(text, reply_markup=ReplyKeyboardRemove())
    await SendPost.file.set()


@dp.message_handler(state=SendPost.file, chat_id=config.ADMINS, content_types=ContentTypes.VIDEO)
async def send_post_def(message: types.Message, state: FSMContext):
    await state.update_data({
        "video": message.video.file_id,
        "image": False
    })

    text = "Post uchun matn kiritasimi ?"
    await message.answer(text, reply_markup=text_or_not)
    await SendPost.text_wait.set()


@dp.callback_query_handler(chat_id=config.ADMINS, text="nothing")
async def send_post_def(call: CallbackQuery, state: FSMContext):
    await state.update_data({
        "video": False,
        "image": False,
    })
    text = "Post uchun matn kiritasimi ?"
    await call.message.answer(text, reply_markup=text_or_not)
    await SendPost.text_wait.set()


@dp.callback_query_handler(state=SendPost.text_wait, chat_id=config.ADMINS, text="send_post_text_yes")
async def send_post_def(call: CallbackQuery):
    text = "Post uchun matnni kiriting."
    await call.message.answer(text, reply_markup=ReplyKeyboardRemove())
    await SendPost.text.set()


@dp.message_handler(state=SendPost.text, chat_id=config.ADMINS)
async def send_post_def(message: types.Message, state: FSMContext):
    await state.update_data({
        "text": message.text
    })

    data = await state.get_data()

    if data.get('image') is False and data.get('video') is False and data.get('text') is False:
        await message.answer("Siz hech qanday parametrlarni kiritmadingiz.", reply_markup=admin_menu)

    answer = "Jo'natishni hohlaysizmi ?"
    await message.answer(answer, reply_markup=send_post)
    await SendPost.waiting.set()


@dp.callback_query_handler(state=SendPost.text_wait, chat_id=config.ADMINS, text="send_post_text_no")
async def send_post_def(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data.get('image') == False and data.get('video') == False:
        text = "Post uchun hech narsa kiritilmadi."
        await call.message.answer(text, reply_markup=admin_menu)
        await state.finish()
    else:
        await state.update_data({
            "text": False
        })
        answer = "Jo'natishni hohlaysizmi ?"
        await call.message.answer(answer, reply_markup=send_post)
        await SendPost.waiting.set()


@dp.callback_query_handler(state=SendPost.waiting, text="send_post_yes", chat_id=config.ADMINS)
async def send_post_yes(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    users = await get_users()
    image = data.get('image')
    video = data.get('video')
    text = data.get('text')
    text_new = "Habar barcha foydalanuvchilarga yuborilmoqda..."
    await call.message.answer(text_new)
    try:
        if users:
            if image and text and video is False:
                for user in users:
                    try:
                        await asyncio.sleep(0.01)
                        await bot.send_photo(chat_id=user["chat_id"], photo=data.get("image"), caption=data.get("text"))
                    except Exception as exc:
                        print(exc)
            elif text is False and image and video is False:
                for user in users:
                    try:
                        await asyncio.sleep(0.01)
                        await bot.send_photo(chat_id=user["chat_id"], photo=data.get("image"))
                    except Exception as exc:
                        print(exc)

            elif text is False and video and image is False:
                for user in users:
                    try:
                        await asyncio.sleep(0.01)
                        await bot.send_video(chat_id=user["chat_id"], video=data.get("video"))
                    except Exception as exc:
                        print(exc)

            elif video and text and image is False:
                for user in users:
                    try:
                        await asyncio.sleep(0.01)
                        await bot.send_video(chat_id=user["chat_id"], video=data.get("video"), caption=data.get("text"))
                    except Exception as exc:
                        print(exc)

            elif video is False and image is False and text:
                for user in users:
                    try:
                        await asyncio.sleep(0.01)
                        await bot.send_message(chat_id=user["chat_id"], text=data.get("text"))
                    except Exception as exc:
                        print(exc)
        else:
            pass

        await state.finish()
        text = "Habar barcha foydalanuvchilarga jo'natildi."
        await call.message.answer(text, reply_markup=admin_menu)
    except Exception as exc:
        print(exc)
        await state.finish()
        text = "Botda nosozlik yuz berdi."
        await call.message.answer(text, reply_markup=admin_menu)


@dp.callback_query_handler(state=SendPost.waiting, text="send_post_no", chat_id=config.ADMINS)
async def send_post_yes(call: CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    await state.finish()
    text = "Habar bekor qilindi."
    await call.message.answer(text, reply_markup=admin_menu)
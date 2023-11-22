from aiogram.types import  KeyboardButton, ReplyKeyboardMarkup

user_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🔗 Maxsus havolam | Махсус ҳаволам")
        ],
        [
            KeyboardButton(text="🚀 Mening natijam | Менинг натижам")
        ]
    ], resize_keyboard=True
)


phone_share = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="☎️ Telefon raqamni jo'natish", request_contact=True)
        ]
    ], resize_keyboard=True
)
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def sharing_referral_def(link: str):
    sharing_referral = InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="Ulashish/Улашиш", switch_inline_query=link)
        ]]
    )
    return sharing_referral


subs_check = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="Tekshirish/Текшириш", callback_data="check_subs")
    ]]
)

send_post = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Jo'natish ⏫", callback_data="send_post_yes"),
            InlineKeyboardButton(text="Bekor qilish ❌", callback_data="send_post_no"),
        ]
    ]
)

image_or_file = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Rasm", callback_data="send_post_image"),
            InlineKeyboardButton(text="Video", callback_data="send_post_file"),
        ],
        [
            InlineKeyboardButton(text="Text", callback_data="nothing")
        ]
    ]
)

text_or_not = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Ha", callback_data="send_post_text_yes"),
            InlineKeyboardButton(text="Yo'q", callback_data="send_post_text_no"),
        ]
    ]
)


start_message_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[[
        InlineKeyboardButton(text="Tayyorman ✅", callback_data="iam_ready")
    ]]
)
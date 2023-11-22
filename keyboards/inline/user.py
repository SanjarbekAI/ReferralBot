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
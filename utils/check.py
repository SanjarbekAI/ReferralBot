from utils.db_api.user_commands import check_referral, add_new_referral, get_user
from loader import dp


async def check_or_add_referral(referral_from: str, referral_to: int):
    try:
        referral_from = int(referral_from)
        referral = await check_referral(referral_from, referral_to)
        if not referral:
            await add_new_referral(referral_from, referral_to)
            referral_user = await get_user(chat_id=referral_to)
            if referral_user:
                text = f"{referral_user['full_name']}, siz ulashgan havola orqali ro'yxatdan o'tdi. 🎉"
            else:
                text = f"Yangi foydalanuvchi siz ulashgan havola orqali ro'yxatdan o'tdi. 🎉"
            await dp.bot.send_message(chat_id=referral_from, text=text)
    except Exception as e:
        error_text = f"Error appeared in adding new referral: {e}"
        print(error_text)


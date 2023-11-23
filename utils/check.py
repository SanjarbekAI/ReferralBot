from main.config import CHANNELS
from utils.db_api.user_commands import check_referral, add_new_referral, get_user
from loader import dp
from utils.misc import subscription


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


async def check_subs(message):
    result = "Botdan foydalanish uchun quyidagi kanalga obuna bo'ling:\n"
    final_status = True
    for channel in CHANNELS:
        status = await subscription.check(user_id=message.chat.id, channel=channel[1])
        if not status:
            final_status = False
            result += f"👉 <a href='{channel[0]}'>{channel[-1]}</a>\n"
    if not final_status:
        return result
    return False


async def check_weight(weight: str):
    try:
        weight = float(weight)
        if 0 > weight > 300:
            return False
        return weight
    except Exception as e:
        print(e)
        return False


from main.models import users, referrals
from main.database_set import database
from main.constants import UserStatus


async def get_users():
    try:
        query = users.select().where(
            users.c.status == UserStatus.active
        )
        rows = await database.fetch_all(query=query)
        return rows if rows else False
    except Exception as e:
        error_text = f"Error apperead when getting users: {e}"
        print(error_text)
        return False



async def get_user(chat_id: int):
    try:
        query = users.select().where(
            users.c.chat_id == chat_id,
            users.c.status == UserStatus.active
        )
        user = await database.fetch_one(query=query)
        return user if user else False
    except Exception as e:
        error_text = f"Error apperead when getting user: {e}"
        print(error_text)
        return False


async def add_user(data: dict):
    try:
        query = users.insert().values(
            full_name=data.get("full_name"),
            phone_number=data.get("phone_number"),
            chat_id=data.get("chat_id"),
            weight=data.get("weight"),
            status=UserStatus.active,
            created_at=data.get("created_at"),
            updated_at=data.get("created_at")
        )
        new_user = await database.execute(query=query)
        return new_user if new_user else False
    except Exception as e:
        error_text = f"Error apperead when getting user: {e}"
        print(error_text)
        return False


async def check_referral(referral_from, referral_to):
    try:
        query = referrals.select().where(
            referrals.c.referral_from == referral_from,
            referrals.c.referral_to == referral_to
        )
        referral = await database.fetch_one(query=query)
        return referral if referral else False
    except Exception as e:
        error_text = f"Error apperead when getting user: {e}"
        print(error_text)
        return False


async def add_new_referral(referral_from, referral_to):
    try:
        query = referrals.insert().values(
            referral_from=referral_from,
            referral_to=referral_to
        )
        referral = await database.fetch_one(query=query)
        return referral if referral else False
    except Exception as e:
        error_text = f"Error apperead when getting user: {e}"
        print(error_text)
        return False


async def get_referrals_count(chat_id: int):
    try:
        query = referrals.select().where(referrals.c.referral_from == chat_id)
        count = await database.fetch_all(query=query)
        return len(count) if count else 0
    except Exception as e:
        error_text = f"Error apperead when getting user: {e}"
        print(error_text)
        return 0

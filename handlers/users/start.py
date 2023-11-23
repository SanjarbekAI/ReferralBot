from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from states.user import RegisterState
from loader import dp
from keyboards.default.user import user_menu, phone_share
from keyboards.inline.user import sharing_referral_def, subs_check, start_message_keyboard
from utils.check import check_or_add_referral, check_subs, check_weight
from utils.db_api.user_commands import get_user, add_user
from main.config import SHARING_CONSTANT

@dp.message_handler(commands="start", state="*")
async def bot_start(message: types.Message, state: FSMContext):
    if await get_user(chat_id=message.chat.id):
        text = "😊 Assalomu alaykum, xush kelibsiz.\nАссалому алайкум, хуш келибсиз."
        await message.answer(text=text, reply_markup=user_menu)
    else:
        referral_from = message.get_args()
        if referral_from:
            await state.update_data(referral_from=referral_from)

        text = ("Assalomu alaykum, shifokor Barno Dietolog bilan 3 kun davomida "
                "amaliyotda ozish chellejida BEPUL ishtirok etish uchun ma'lumotlarni"
                " aniq kiriting, chunki ANALIZ va DIAGNOSTIKA paytida bu juda ham muhim."
                " Tayyormisiz?")
        await message.answer(text=text, reply_markup=start_message_keyboard)


@dp.callback_query_handler(text="iam_ready")
async def iam_ready_handler(call: types.CallbackQuery):
    text = "Iltimos ism familiyangizni kiriting.\nИлтимос исм фамилиянгизни киритинг."
    await call.message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await RegisterState.full_name.set()


@dp.message_handler(state=RegisterState.full_name)
async def get_full_name_handler(message: types.Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    text = ("Iltimos pastdagi tugmadan foydalangan holda telefon raqamingizni kiriting.\n"
            "Илтимос пастдаги тугмадан фойдаланган ҳолда телефон рақамингизни киритинг.")
    await message.answer(text=text, reply_markup=phone_share)
    await RegisterState.phone_number.set()


@dp.message_handler(state=RegisterState.phone_number, content_types=types.ContentType.CONTACT)
async def get_contact_handler(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.contact.phone_number)
    text = "Iltimos taxminiy vazningizni kiriting\nИлтимос тахминий вазнингизни киритинг"
    await message.answer(text=text, reply_markup=ReplyKeyboardRemove())
    await RegisterState.weight.set()


@dp.message_handler(state=RegisterState.weight)
async def get_weight_handler(message: types.Message, state: FSMContext):
    weight = await check_weight(weight=message.text)
    if weight:
        await state.update_data(weight=weight, chat_id=message.chat.id, created_at=message.date)
        data = await state.get_data()

        new_user = await add_user(data)
        if new_user:
            text = "✅ Muvafaqqiyatli ro'yxatdan o'tdingiz\nМувафаққиятли рўйхатдан ўтдингиз."
            await message.answer(text=text, reply_markup=user_menu)

            result = await check_subs(message)
            if result:
                await message.answer(result, disable_web_page_preview=True, reply_markup=subs_check)
            else:
                link = f"{SHARING_CONSTANT}{message.chat.id}"
                text = ("✅ Sizning maxsus havolangiz. Bu havolani do'stlaringizga yuboring va 10 ta"
                        " ortiqcha vaznga ega do'stingizni taklif qiling. Bu orqali siz shifokor-dietolog"
                        " Barno Suleymanova bilan 3 kunda amaliyotda rostan ham ozish chellenjida "
                        "BEPUL ishtirok eta olasiz 👇")
                await message.answer(text=text, reply_markup=await sharing_referral_def(link))
        else:
            text = ("❌ Botda muommo mavjud. Iltimos bizga aloqaga chiqing.\n"
                    "Ботда муоммо мавжуд. Илтимос бизга алоқага чиқинг.")
            await message.answer(text=text, reply_markup=ReplyKeyboardRemove())

        referral_from = data.get('referral_from')
        if referral_from:
            await check_or_add_referral(referral_from, message.chat.id)

        await state.finish()
    else:
        text = "❌ Iltimos to'g'ri qiymat kiriting\nИлтимос тўғри қиймат киритинг"
        await message.answer(text=text)
        await RegisterState.weight.set()



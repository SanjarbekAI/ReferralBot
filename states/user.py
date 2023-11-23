from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterState(StatesGroup):
    full_name = State()
    phone_number = State()
    weight = State()


class SendPost(StatesGroup):
    image_or_file = State()
    image = State()
    file = State()
    text = State()
    text_wait = State()
    link = State()
    button_text = State()
    waiting = State()
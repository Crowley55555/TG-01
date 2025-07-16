from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

kb = ReplyKeyboardMarkup(  # Создание клавиатуры
    keyboard=[
        [KeyboardButton(text='📝 Тестовая кнопка 1')], # Создание кнопки
        [ KeyboardButton(text='📝 Тестовая кнопка 2'), KeyboardButton(text='📝 Тестовая кнопка 3')]  # Создание кнопки
        ], resize_keyboard=True) # Размер кнопок

inline_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📝 каталог', callback_data='catalog')], # Создание кнопки инлайн
    [InlineKeyboardButton(text='📝 новости', callback_data='news')],
    [InlineKeyboardButton(text='📝 профиль', callback_data='profile')],

])

test = ["📝 кнопка 1", "📝  кнопка 2", "📝 кнопка 3", "📝 кнопка 4"]


async def test_keyboard():
    kb1 = InlineKeyboardBuilder()
    for key in test:
        # kb1.button(text=key) # Создание кнопки
        kb1.add(InlineKeyboardButton(text=key,url = 'https://fors-mazhory-lordserial.ru/')) # Создание кнопки
    return kb1.adjust(2).as_markup(resize_keyboard=True)

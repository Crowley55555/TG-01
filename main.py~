import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from config import TOKEN

import random
import aiohttp
from config import WEATHER_API_KEY
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from gtts import gTTS
import os
import re
from deep_translator import GoogleTranslator


bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('doc'))
async def doc(message: Message):
    doc = FSInputFile('file.pdf')
    await bot.send_document(message.chat.id, doc)

@dp.message(Command('video'))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, action='upload_video')
    video = FSInputFile('video.mp4')
    await bot.send_video(message.chat.id, video)

@dp.message(Command('voice'))
async def voice(message: Message):
    await bot.send_chat_action(message.chat.id, action='upload_voice')
    voice = FSInputFile('voice.ogg')
    await message.answer_voice(voice)


@dp.message(Command('audio'))
async def audio(message: Message):
    await bot.send_chat_action(message.chat.id, action='upload_audio')
    audio = FSInputFile('Dirty Magic.m4a')
    await bot.send_audio(message.chat.id, audio)

@dp.message(Command('training'))
async def training(message: Message):

    traning_list = [
        {
            "title": "💪 <b>Силовая тренировка (5на5)</b>",
            "description": (
                "<i>Цель:</i> Увеличение силы в базовых упражнениях\n\n"
                "🏋️ <b>Приседания со штангой</b> – 5 подходов по 5 раз\n"
                "🛌 <b>Жим штанги лёжа</b> – 5 подходов по 5 раз\n"
                "⬆️ <b>Становая тяга</b> – 3 подхода по 5 раз\n"
                "🙌 <b>Подтягивания</b> – 3 подхода по максимуму\n"
                "⏱ <b>Планка</b> – 3 подхода по 60 секунд"
            )
        },
        {
            "title": "🔥 <b>Круговая тренировка (3 круга)</b>",
            "description": (
                "<i>Цель:</i> Выносливость и жиросжигание\n\n"
                "🐸 <b>Бёрпи</b> – 15 раз\n"
                "🏃 <b>Прыжки на скакалке</b> – 1 минута\n"
                "✊ <b>Отжимания</b> – 20 раз\n"
                "🦵 <b>Приседания с прыжком</b> – 20 раз\n"
                "🧗 <b>Скалолаз</b> – 30 секунд\n"
                "⏱ <b>Планка</b> – 45 секунд"
            )
        },
        {
            "title": "📅 <b>Сплит-тренировка (3 дня)</b>",
            "description": (
                "<i>День 1 (Грудь + Трицепс):</i>\n"
                "🛌 <b>Жим штанги лёжа</b> – 4 подхода по 8 раз\n"
                "✈️ <b>Разводка гантелей</b> – 3 подхода по 12 раз\n"
                "👇 <b>Отжимания на брусьях</b> – 3 подхода по максимуму\n"
                "💪 <b>Французский жим</b> – 4 подхода по 10 раз\n\n"

                "<i>День 2 (Спина + Бицепс):</i>\n"
                "🙌 <b>Подтягивания</b> – 4 подхода по максимуму\n"
                "🏋️ <b>Тяга штанги в наклоне</b> – 4 подхода по 8 раз\n"
                "👜 <b>Тяга гантели одной рукой</b> – 3 подхода по 10 раз\n"
                "💪 <b>Подъём штанги на бицепс</b> – 3 подхода по 12 раз\n\n"

                "<i>День 3 (Ноги + Плечи):</i>\n"
                "🦵 <b>Приседания со штангой</b> – 4 подхода по 8 раз\n"
                "⬆️ <b>Румынская тяга</b> – 3 подхода по 10 раз\n"
                "🪑 <b>Жим гантелей сидя</b> – 4 подхода по 10 раз\n"
                "✈️ <b>Махи в стороны</b> – 3 подхода по 15 раз"
            )
        }
    ]
    rand_tr = random.choice(traning_list)
    await message.answer(rand_tr['title'], parse_mode='HTML')
    await message.answer(rand_tr['description'], parse_mode='HTML')

    await bot.send_chat_action(message.chat.id, action='upload_audio')

    # Очищаем текст от HTML-тегов и эмодзи
    clean_text = re.sub('<[^<]+?>', '', rand_tr['description'])  # Удаляем HTML-теги
    clean_text = re.sub(r'[^\w\s.,!?-]', '', clean_text)  # Удаляем эмодзи и спецсимволы

    tts = gTTS(text=clean_text, lang='ru')
    tts.save(f'tmp/{message.from_user.id}.ogg')
    audio = FSInputFile(f'tmp/{message.from_user.id}.ogg')
    await bot.send_voice(message.chat.id, audio)
    os.remove(f'tmp/{message.from_user.id}.ogg')

@dp.message(F.text == 'Что такое ИИ')
async def aitext(message: Message):
    await message.answer('ИИ - это интеллектуальный инструмент, который может выполнять различные задачи и обрабатывать информацию')

@dp.message(F.photo)
async def reactphoto(message: Message):
    list = ['норм фотка', 'непонятно что это', 'пришли еще такую фотку']
    rand_answer = random.choice(list)
    await message.answer(rand_answer)
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')

@dp.message(Command('photo'))
async def photo(message: Message):
    list = [
        'https://ru.freepik.com/premium-photo/curved-steel-abstract-wallpaper-blue-ribbed-metal-3d-render_35146939.htm#fromView=keyword&page=1&position=5&uuid=27689733-362c-4bfe-8e9f-2d4cba254921&query=%D0%90%D0%B1%D1%81%D1%82%D1%80%D0%B0%D0%BA%D1%86%D0%B8%D0%B8',
        'https://ru.freepik.com/free-photo/stylish-blue-curve-lines-abstract-background_15829525.htm#fromView=keyword&page=1&position=41&uuid=27689733-362c-4bfe-8e9f-2d4cba254921&query=%D0%90%D0%B1%D1%81%D1%82%D1%80%D0%B0%D0%BA%D1%86%D0%B8%D0%B8',
        'https://ru.freepik.com/free-photo/elegant-smooth-wavy-lines-flow-background_15829559.htm#fromView=image_search_similar&page=1&position=15&uuid=82b79214-f1cf-4191-9c8b-2d3b4567e112&query=%D0%90%D0%B1%D1%81%D1%82%D1%80%D0%B0%D0%BA%D1%86%D0%B8%D0%B8'
    ]
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption='это фотка')

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('этот бот умеет выполнять команды \n /start - приветствие \n /help - помощь \n /photo - фотография\n /weather <город> - прогноз погоды')

class WeatherStates(StatesGroup):
    waiting_for_city = State()

@dp.message(Command('weather'))
async def weather_command(message: Message, state: FSMContext):
    await message.answer('Пожалуйста, введите название города для прогноза погоды:')
    await state.set_state(WeatherStates.waiting_for_city)

@dp.message(WeatherStates.waiting_for_city)
async def process_city(message: Message, state: FSMContext):
    city = message.text.strip()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                await message.answer('Не удалось получить данные о погоде. Проверьте название города.')
                await state.clear()
                return
            data = await resp.json()
            if data.get('cod') != 200:
                await message.answer('Город не найден. Попробуйте еще раз.')
                await state.clear()
                return
            weather_desc = data['weather'][0]['description'].capitalize()
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            answer = (f"Погода в городе {city}:\n"
                      f"{weather_desc}\n"
                      f"Температура: {temp}°C (ощущается как {feels_like}°C)\n"
                      f"Влажность: {humidity}%\n"
                      f"Ветер: {wind_speed} м/с")
            await message.answer(answer)
    await state.clear()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет {message.from_user.full_name}, я бот!')

@dp.message(F.text.lower() == 'тест')
async def test(message: Message):
    await message.answer('Запускаем тестирование')

# @dp.message()
# async def echo(message: Message):
#     await message.send_copy(chat_id=message.from_user.id)

@dp.message(F.text & ~F.text.startswith('/'))
async def translate_to_english(message: Message):
    text = message.text
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        await message.answer(translated)
    except Exception as e:
        await message.answer(f"Ошибка при переводе: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
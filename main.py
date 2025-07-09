import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import TOKEN

import random
import aiohttp
from config import WEATHER_API_KEY
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

bot = Bot(token=TOKEN)
dp = Dispatcher()



@dp.message(F.text == 'Что такое ИИ')
async def aitext(message: Message):
    await message.answer('ИИ - это интеллектуальный инструмент, который может выполнять различные задачи и обрабатывать информацию')

@dp.message(F.photo)
async def reactphoto(message: Message):
    list = ['норм фотка', 'непонятно что это', 'пришли еще такую фотку']
    rand_answer = random.choice(list)
    await message.answer(rand_answer)

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
    await message.answer('Привет, я бот!')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
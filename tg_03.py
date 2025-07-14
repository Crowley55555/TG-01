import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
from config import WEATHER_API_KEY
import sqlite3
import aiohttp
import logging


bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    name = State()
    age = State()
    city = State()

def init_db():
    conn = sqlite3.connect('tg_03.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        age INTEGER,
        city TEXT NOT NULL
    )""")
    conn.commit()
    conn.close()

init_db()

@dp.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?")  # Приветствие и запрос имени
    await state.set_state(Form.name)  # Установка состояния - ожидание имени

@dp.message(Form.name)
async def process_name(message: Message, state: FSMContext): # Обработка имени
    await state.update_data(name=message.text)  # Сохранение имени в базе данных
    await message.answer("Сколько тебе лет?") # Запрос возраста
    await state.set_state(Form.age)  # Установка состояния - ожидание возраста

@dp.message(Form.age)
async def process_age(message: Message, state: FSMContext): # Обработка возраста
    await state.update_data(age=message.text)  # Сохранение возраста в базе данных
    await message.answer("В каком городе ты живешь?") # Запрос города
    await state.set_state(Form.city)  # Установка состояния - ожидание города

@dp.message(Form.city)
async def process_city(message: Message, state: FSMContext): # Обработка города
    await state.update_data(city=message.text)  # Сохранение города в базе данных
    user_data = await state.get_data()  # Получение сохраненных данных

    conn = sqlite3.connect('tg_03.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO users (username, age, city) VALUES (?, ?, ?)''', (user_data['name'], user_data['age'], user_data['city']))

    conn.commit()
    conn.close()

    # async with aiohttp.ClientSession() as session:
    #     async with session.get(f"http://api.openweathermap.org/data/2.5/weather?q={user_data['city']}&appid={WEATHER_API_KEY}&units=metric&lang=ru") as response:
    #         if response.status == 200:
    #             weather_data = await response.json()
    #             main = weather_data['main']
    #             weather = weather_data['weather'][0]
    #
    #             temp = main['temp']
    #             feels_like = main['feels_like']
    #             humidity = main['humidity']
    #             wind_speed = weather_data['wind']['speed']
    #             answer = (f"Погода в городе {user_data['city']}:\n"
    #                       f"{weather['description'].capitalize()}\n"
    #                       f"Температура: {temp}°C (ощущается как {feels_like}°C)\n"
    #                       f"Влажность: {humidity}%\n"
    #                       f"Ветер: {wind_speed} м/с")
    #             await message.answer(answer)
    #         else:
    #             await message.answer('Не удалось получить данные о погоде. Проверьте название города.')
    #             await state.clear()
    #             return

    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://api.openweathermap.org/data/2.5/weather?q={user_data['city']}&appid={WEATHER_API_KEY}&units=metric&lang=ru") as response:
            if response.status != 200:
                await message.answer('Не удалось получить данные о погоде. Проверьте название города.')
                await state.clear()
                return

            weather_data = await response.json()

        if weather_data.get('cod') != 200:
            await message.answer('Город не найден. Попробуйте еще раз.')
            await state.clear()
            return
        weather_desc = weather_data['weather'][0]['description'].capitalize()
        temp = weather_data['main']['temp']
        feels_like = weather_data['main']['feels_like']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']

        answer = (f"Погода в городе {user_data['city']}:\n"
                    f"{weather_desc}\n"
                    f"Температура: {temp}°C (ощущается как {feels_like}°C)\n"
                    f"Влажность: {humidity}%\n"
                    f"Ветер: {wind_speed} м/с")

        await message.answer(answer)

        await state.clear()





async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv
import os

import sqlite3

import logging

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)

dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()

def init_db():
    conn = sqlite3.connect('school_data.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        age INTEGER,
        grade TEXT NOT NULL
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
    await message.answer("В каком классе ты учишься?") # Запрос города
    await state.set_state(Form.grade)  # Установка состояния - ожидание города

@dp.message(Form.grade)
async def process_grade(message: Message, state: FSMContext): # Обработка класса
    await state.update_data(grade=message.text)  # Сохранение класса в базе данных
    user_data = await state.get_data()  # Получение сохраненных данных

    conn = sqlite3.connect('school_data.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO students (username, age, grade) VALUES (?, ?, ?)''', (user_data['name'], user_data['age'], user_data['grade']))

    conn.commit()
    conn.close()

    await message.answer("Спасибо за регистрацию! Ваши данные успешно сохранены: \n"
                         f"Имя: {user_data['name']}\n"
                         f"Возраст: {user_data['age']}\n"
                         f"Класс: {user_data['grade']}")

    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

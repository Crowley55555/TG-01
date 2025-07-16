import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN
from keyboards import kb, inline_kb
import keyboards as kbb

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.callback_query(F.data == 'news')
async def news(call: CallbackQuery):
    await call.answer('Новости отправлены', show_alert=True)
    await call.message.edit_text('Вот твои Новости', reply_markup=await kbb.test_keyboard())


@dp.message(F.text == '📝 кнопка 1')
async def test_button(message: Message):
    await message.answer('Вы нажали кнопку 1')

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет {message.from_user.full_name}, я бот!', reply_markup=inline_kb) # Приветствие и запрос имени для обычных кнопок
    # await message.answer(f'Привет {message.from_user.full_name}, я бот!',
    #                      reply_markup=await kbb.test_keyboard())  # для ButtonBuilder клавиатуры

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
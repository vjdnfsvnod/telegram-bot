import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor

# Введи свій токен від BotFather тут
import os
TOKEN = os.getenv("BOT_TOKEN")


# Увімкнення логування (для відстеження помилок)
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Функція розрахунку чайових
def calculate_tips(amount):
    dishwasher = round(amount * 0.2, 2)
    waiter1 = round(amount * 0.4, 2)
    waiter2 = round(amount * 0.4, 2)
    return dishwasher, waiter1, waiter2

# Команда /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    await message.reply("Привіт! Введи суму чайових, і я поділю її між персоналом.")

# Обробка введених чисел
@dp.message_handler(lambda message: message.text.isdigit())
async def handle_tip_amount(message: Message):
    amount = float(message.text)
    dishwasher, waiter1, waiter2 = calculate_tips(amount)
    response = (
        f"Розподіл чайових:\n"
        f"🍽 Посудомийка: {dishwasher}$\n"
        f"👨‍🍳 Офіціант 1: {waiter1}$\n"
        f"👩‍🍳 Офіціант 2: {waiter2}$"
    )
    await message.reply(response)

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor

import os

# Отримуємо токен з Render (або заміни "YOUR_BOT_TOKEN" своїм токеном)
TOKEN = os.getenv("BOT_TOKEN")

# Увімкнення логування
logging.basicConfig(level=logging.INFO)

# Ініціалізація бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Функція розрахунку чайових
def calculate_tips(amount):
    amount = round(amount, 2)  # Округлюємо введену суму до копійок
    dishwasher_share = amount * 0.2  # 20% мийці
    waiter_share = (amount - dishwasher_share) / 2  # 40% кожному офіціанту

    # Округлюємо вниз частку офіціантів до копійок
    waiter_share = round(waiter_share, 2)
    dishwasher_share = round(amount - (waiter_share * 2), 2)  # Всі залишки йдуть мийці

    return dishwasher_share, waiter_share, waiter_share

# Команда /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    await message.reply("Привіт! Введи суму чайових (наприклад, 100.50), і я поділю її між персоналом.")

# Обробка введених чисел
@dp.message_handler(lambda message: message.text.replace('.', '', 1).isdigit())
async def handle_tip_amount(message: Message):
    amount = float(message.text)
    dishwasher, waiter1, waiter2 = calculate_tips(amount)
    response = (
        f"💰 **Розподіл чайових:**\n"
        f"🍽 Посудомийка: **{dishwasher}$**\n"
        f"👨‍🍳 Офіціант 1: **{waiter1}$**\n"
        f"👩‍🍳 Офіціант 2: **{waiter2}$**"
    )
    await message.reply(response, parse_mode="Markdown")

# Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

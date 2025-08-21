import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("support"))
async def support(message: types.Message):
    await message.answer("Служба поддержки временно не работает :)")

@dp.message(Command("report"))
async def report(message: types.Message):
    await message.answer("Бот работает!")    

@dp.message()
async def send_way(message: types.Message):
    await message.answer("Для формирования отчета, нажмите кнопку Меню")    

if __name__ == "__main__":
    dp.run_polling(bot)
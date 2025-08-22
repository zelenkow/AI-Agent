import os
import logging
import aiohttp
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CLIENT_ID = os.getenv("AVITO_CLIENT_ID")
CLIENT_SECRET = os.getenv("AVITO_CLIENT_SECRET")
DIKON_ID = os.getenv("DIKON_USER_ID")

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def get_avito_token():
    data_api = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.avito.ru/token",
            data=data_api,
        ) as response:
            token_data = await response.json()
            return token_data["access_token"]

@dp.message(Command("report"))
async def report(message: types.Message):
    token = await get_avito_token()
    await message.answer(f"Токен получен: {token}") 

@dp.message()
async def send_way(message: types.Message):
    #print(message.model_dump_json(indent=4, exclude_none=True))  Для вывода JSON только с активными параметрами
    await message.answer("Для формирования отчета, нажмите Меню и выберите Сформировать отчет")

if __name__ == "__main__":
    dp.run_polling(bot)
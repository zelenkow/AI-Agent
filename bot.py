import os
import logging
import aiohttp
from cachetools import TTLCache
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

token_cache = TTLCache(maxsize=1, ttl=23.5 * 60 * 60)

async def get_avito_token():

    if 'avito_token' in token_cache:
        logger.info("Используется кешированный токен Avito")
        return token_cache['avito_token']
    logger.info("Запрашивается новый токен Avito")
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
            new_token = token_data["access_token"]
            token_cache['avito_token'] = new_token
            return new_token
        
async def get_avito_chats(access_token):
    headers =  {'Authorization': f'Bearer {access_token}'}
    params = {'limit': 3,'offset': 0}
    url = f"https://api.avito.ru/messenger/v2/accounts/{DIKON_ID}/chats"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                raw_chats = await response.json()
                return raw_chats
            else:
                logger.error(f"Ошибка получения чатов: {response.status}")
                return {}
            
async def get_avito_messages(access_token, chat_id):
    headers = {'Authorization': f'Bearer {access_token}'}
    params = {'limit': 100, 'offset': 0}
    url = f"https://api.avito.ru/messenger/v1/accounts/{DIKON_ID}/chats/{chat_id}/messages"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status == 200:
                raw_messages = await response.json()
                return raw_messages
            else:
                logger.error(f"Ошибка получения сообщений: {response.status}")
                return {}
            
def map_avito_chats(raw_chats_data, my_user_id):
    mapped_chats = []
    
    for chat in raw_chats_data.get('chats', []):
        client_name = 'Неизвестный клиент'
        for user in chat.get('users', []):
            if user.get('id') != my_user_id and user.get('name'):
                client_name = user['name']
                break

        mapped_chat = {
            'chat_id': chat.get('id', 'Без названия'),
            'title': chat.get('context', {}).get('value', {}).get('title', 'Без названия'),
            'client_name': client_name,
            'created_at': chat.get('created', 0),
            'updated_at': chat.get('updated', 0)
        }
        mapped_chats.append(mapped_chat)
    
    return mapped_chats

@dp.message(Command("report"))
async def report(message: types.Message):
    token = await get_avito_token()
    await message.answer(f"Токен получен: {token}")
    raw_data_chats = await get_avito_chats(token)
    await message.answer(f"Сырые данные чата получены")
    map_data_chats = map_avito_chats(raw_data_chats, DIKON_ID)  
    await message.answer(str(map_data_chats))

@dp.message()
async def send_way(message: types.Message):
    await message.answer("Для формирования отчета, нажмите Меню и выберите Сформировать отчет")

if __name__ == "__main__":
    dp.run_polling(bot)
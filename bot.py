import logging
import asyncio
import os 
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
import datetime

# Базовая настройка логирования
logging.basicConfig(level=logging.INFO)

# Токен вашего бота
TOKEN = os.getenv("TOKEN")

# Бот и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

t = {'ё': 'yo', 'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ж': 'zh',
     'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
     'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh',
     'щ': 'shch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya'}

def transliterate(text):
    result = []
    for char in text.lower():
        if char in t:
            result.append(t[char])
        elif char == ' ':
            result.append(' ')
        else:
            result.append('-')
    return ''.join(result).title()

# Функция для логирования в файл
def log_to_file(user_id, username, original_fio, transliterated_fio):
    with open('transliteration_log.txt', 'a', encoding='utf-8') as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} | User: {user_id} ({username}) | Original: {original_fio} | Transliterated: {transliterated_fio}\n")

# Обработчик команды "/start" 
@dp.message(CommandStart())
async def start_command_handler(message: types.Message):
    await message.answer("Привет! Введите Фамилию Имя Отчество.")

@dp.message()
async def handler_fio(message: types.Message):
    try:
        fio = message.text.strip()
        if not fio:
            await message.answer("Пожалуйста, введите ФИО")
            return
            
        transliterated_fio = transliterate(fio)
        
        # Логирование в файл
        log_to_file(
            message.from_user.id, 
            message.from_user.username or "No username", 
            fio, 
            transliterated_fio
        )
        
        await message.answer(transliterated_fio)
        
    except Exception as e:
        logging.error(f"Error processing message: {e}")
        await message.answer("Произошла ошибка при обработке ФИО")

# Главная функция для запуска бота
async def main():
    await dp.start_polling(bot)

# Проверяем, запущен ли сценарий 
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
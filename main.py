import asyncio
from datetime import datetime
import logging
import os

from aiogram import Bot
from dotenv import load_dotenv

from currency import get_currency


async def main():
    load_dotenv()
    token = os.getenv('BOT_TOKEN')
    bot = Bot(token)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='log.log',
    )
    while True:
        if datetime.today().hour == 10:
            try:
                currency = get_currency()
            except Exception as e:
                logging.error(e)
                await asyncio.sleep(10)
            else:
                await bot.send_message(343798461, text=f'Покупка: {currency[0]}\nПродажа: {currency[1]}')
                await asyncio.sleep(3600)


if __name__ == '__main__':
    logging.info('Бот запущен')
    asyncio.run(main())

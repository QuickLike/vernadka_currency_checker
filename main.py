import asyncio
from datetime import datetime
import logging
import os
import sys

from aiogram import Bot
from dotenv import load_dotenv

import constraints
from currency import get_currency

bot_work_type = constraints.UPDATES
# UPDATES - присылать данные при обновлении на сайте
# SCHEDULE - по расписанию, время отправки берется из константы SEND_TIME

SEND_TIME = 10
# Время указывается в часах


async def main():
    load_dotenv()
    token = os.getenv('BOT_TOKEN', '')
    user_id = os.getenv('USER_ID', '')
    bot = Bot(token)
    try:
        currency = get_currency()
    except Exception as e:
        logging.error(e)
        return
    while True:
        if bot_work_type == constraints.UPDATES:
            await asyncio.sleep(10)
            if currency != get_currency():
                currency = get_currency()
                logging.info(constraints.SEND_MESSAGE.format(currency=currency))
                await bot.send_message(
                    chat_id=user_id,
                    text=constraints.SEND_MESSAGE.format(currency=currency)
                )
        elif bot_work_type == constraints.SCHEDULE:
            if not isinstance(SEND_TIME, int):
                raise ValueError(f'Переменная SEND_TIME должна быть целочисленной.\n{SEND_TIME=}')
            if datetime.today().hour == SEND_TIME:
                logging.info(constraints.SEND_MESSAGE.format(currency=currency))
                await bot.send_message(
                    chat_id=user_id,
                    text=constraints.SEND_MESSAGE.format(currency=currency)
                )
                await asyncio.sleep(3600)
        else:
            raise TypeError(f'Неизвестный тип работы бота! {bot_work_type=}\nДопустимые типы: updates, schedule')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format=('%(asctime)s, '
                '%(levelname)s, '
                '%(funcName)s, '
                '%(lineno)d, '
                '%(message)s'
                ),
        encoding='UTF-8',
        handlers=[logging.FileHandler(__file__ + '.log'),
                  logging.StreamHandler(sys.stdout)]
    )
    logging.info('Бот запущен')
    asyncio.run(main())

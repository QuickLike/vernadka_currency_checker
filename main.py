import asyncio
from datetime import datetime
import logging
import sys

from aiogram.filters import Command
from aiogram.types import FSInputFile, Message

import constraints
from currency import get_currency
from plot import draw_graph


bot_work_type = constraints.UPDATES
# UPDATES - присылать данные при обновлении на сайте
# SCHEDULE - по расписанию, время отправки берется из константы SEND_TIME

SEND_TIME = 23
# Время указывается в часах


@constraints.dp.message(Command('get'))
async def get_currencies(message: Message):
    for currency in get_currency().items():
        await message.answer(
            text=constraints.SEND_MESSAGE.format(currency=currency),
            parse_mode='HTML'
        )
        await asyncio.sleep(2)


async def check_and_send():
    try:
        currencies = get_currency()
    except Exception as e:
        logging.error(e)
        return
    while True:
        if bot_work_type == constraints.UPDATES:
            await asyncio.sleep(10)
            if currencies != get_currency():
                currencies = get_currency()
                for currency in currencies.items():
                    # db.insert_currencies(currency)
                    logging.info('\n' + constraints.SEND_MESSAGE.format(currency=currency))
                    await constraints.bot.send_message(
                        chat_id=constraints.USER_ID,
                        text=constraints.SEND_MESSAGE.format(currency=currency),
                        parse_mode='HTML'
                    )
                    await asyncio.sleep(2)
        elif bot_work_type == constraints.SCHEDULE:
            if not isinstance(SEND_TIME, int):
                raise ValueError(f'Переменная SEND_TIME должна быть целочисленной.\n{SEND_TIME=}')
            if datetime.today().hour == SEND_TIME:
                for currency in currencies.items():
                    # db.insert_currencies(currency)
                    logging.info('\n' + constraints.SEND_MESSAGE.format(currency=currency))
                    await constraints.bot.send_message(
                        chat_id=constraints.USER_ID,
                        text=constraints.SEND_MESSAGE.format(currency=currency),
                        parse_mode='HTML'
                    )
                await asyncio.sleep(3600)
        else:
            raise TypeError(f'Неизвестный тип работы бота! {bot_work_type=}\nДопустимые типы: updates, schedule')

        # if datetime.today().hour == 0 and datetime.today().weekday() == 5:
        #     currencies = db.get_weekly_currencies()
        #     file_name = draw_graph(currencies, interval='weekly')
        #     await bot.send_photo(
        #         chat_id=user_id,
        #         photo=FSInputFile(file_name),
        #         caption='График изменения курса $ за прошедшую неделю.',
        #     )
        #     await asyncio.sleep(3600)
        # elif datetime.today().hour == 0 and datetime.today().weekday() not in [0, 5, 6]:
        #     currencies = db.get_daily_currencies()
        #     file_name = draw_graph(currencies, interval='daily')
        #     await bot.send_photo(
        #         chat_id=user_id,
        #         photo=FSInputFile(file_name),
        #         caption='График изменения курса $ за прошедший день.',
        #     )
        #     await asyncio.sleep(3600)


async def main():
    bot = asyncio.get_event_loop().create_task(constraints.dp.start_polling(constraints.bot))
    currency = asyncio.get_event_loop().create_task(check_and_send())
    await asyncio.wait([bot, currency])



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
    asyncio.get_event_loop().run_until_complete(main())

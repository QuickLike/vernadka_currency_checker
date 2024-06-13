import datetime
import sqlite3


week_days = ('Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье')


class Database:
    def __init__(self, db_name='db.sqlite3'):
        self.db_name = db_name
        with sqlite3.connect(db_name) as conn:
            cur = conn.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS currencies (buy_amount REAL, sell_amount REAL, change_date TEXT, '
                        'week_day TEXT)')
            conn.commit()

    def insert_currencies(self, currencies):
        buy_amount, sell_amount = currencies
        now = datetime.datetime.now()
        week_day = week_days[now.weekday()]
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            cur.execute('INSERT INTO currencies (buy_amount, sell_amount, change_date, week_day) VALUES (?, ?, ?, ?)', (buy_amount, sell_amount, now, week_day))
            conn.commit()

    def get_daily_currencies(self):
        today_9am = str(datetime.date.today()) + ' ' + '09:00:00'
        today_10pm = str(datetime.date.today()) + ' ' + '22:00:00'
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            currencies = cur.execute('SELECT * FROM currencies WHERE DATE(change_date) = date(?, "-1 day")', (datetime.date.today(), )).fetchall()
            conn.commit()
            return currencies

    def get_weekly_currencies(self):
        today = datetime.datetime.now()
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            currencies = cur.execute('SELECT * FROM currencies WHERE change_date BETWEEN ? AND ?', (today - datetime.timedelta(6), today)).fetchall()
            conn.commit()
            return currencies

    def get_all_currencies(self):
        with sqlite3.connect(self.db_name) as conn:
            cur = conn.cursor()
            currencies = cur.execute('SELECT * FROM currencies').fetchall()
            conn.commit()
            return currencies


def main():
    db = Database()
    db.insert_currencies((88.50, 90.50))
    # print(db.get_weekly_currencies())
    print(db.get_daily_currencies())
    # print(db.get_weekly_currencies())


if __name__ == '__main__':
    main()

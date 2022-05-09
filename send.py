import telebot
import schedule
from settings import bot_token
from achivevements import ach
from count import count
import time
import sqlite3
import datetime
conn = sqlite3.connect('telegramid.sqlite', check_same_thread=False)
cur = conn.cursor()


# Бот отправляет всем пользователям каждый день информацию о их прогрессе
def job(bot):
    cur.execute("SELECT * FROM users;")
    all_results = cur.fetchall()
    for s in all_results:
        x = s[1].split()
        x = list(map(int, x[0].split('-') + x[1].split(':')))
        date_1 = datetime.datetime(x[0], x[1], x[2], x[3], x[4], x[5])
        delta = datetime.datetime.now() - date_1
        h = str(delta).split()[0]
        try:
            if str(delta).split('.')[0].split()[2] == '0:00:00':
                cur.execute("UPDATE users SET days = ? WHERE userid = ?", (int(str(delta).split()[0]), s[0]))
                conn.commit()
                bot.send_message(s[0], "Поздравляю! У вас " + str(delta).split()[0] + count(int(h)) + "Так держать!!!")
                # Если пользователь достиг определённого рез-та, то ему присваивается звание
                if int(h) in [1, 3, 5, 7, 10, 14, 21, 30, 60, 90, 120, 150, 180, 240, 300, 365, 500]:
                    cur.execute("UPDATE users SET ach = ? WHERE userid = ?", (ach(h), s[0]))
                    conn.commit()
                    bot.send_message(s[0], "Получено новое достижение: " + ach(h))

        except IndexError:
            pass


# Бот выполняет свою работу каждую секунду
bot = telebot.TeleBot(bot_token)
schedule.every(1).seconds.do(job, bot)
# Бот работает всегда
while True:
    schedule.run_pending()
    time.sleep(1)

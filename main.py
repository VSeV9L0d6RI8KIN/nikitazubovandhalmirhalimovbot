import telebot
from settings import bot_token
import sqlite3
import datetime
from achivevements import ach
from count import count
import os
bot = telebot.TeleBot(bot_token)
user_id = 0
now = datetime.datetime.now()
flag = False
# Подключение к БД
conn = sqlite3.connect('telegramid.sqlite', check_same_thread=False)
# Создание курсора
cur = conn.cursor()
# Создание таблицы в БД
cur.execute("""CREATE TABLE IF NOT EXISTS users(
   userid INT,
   btime TEXT,
   days INT,
   ach TEXT);
""")
bot_token = os.environ['BOT_TOKEN']


# Проверка - есть ли пользователь в базе
def if_user_in_the_db(user):
    global cur, conn
    cur.execute("SELECT * FROM users")
    all_results = cur.fetchall()
    for i in all_results:
        if user in i:
            return True


# Информация о боте
@bot.message_handler(commands=['info'])
def start(message):
    global user_id
    user_id = message.chat.id
    bot.send_message(user_id, "СуперЖелезнаяВоля - обычный телеграм-бот, который поможет вам избавиться от вредных"
                              " привычек. Он способен мотивировать вас, постоянно напоминая вам о вашем прогрессе. "
                              "Чтобы управлять ботом, используйте следующие команды:" + "\n" +
                              "     /start - Начать действовать!" + "\n" +
                              "     /getdays - Узнать о вашем прогрессе" + "\n" +
                              "     /restart - Начать заново" + "\n" +
                              "     /setstarttime - Установить новое время начала" + "\n" +
                              "     /end - Закончить и сдаться" + "\n" +
                              "     /info - Узнать информацию о боте" + "\n"
                              "За свой 'труд' вы будете получать достижения:" + "\n" +
                              "     Разведчик - 1 день" + "\n" +
                              "     Рядовой - 3 дня" + "\n" +
                              "     Капрал - 5 дней" + "\n" +
                              "     Сержант - 7 дней" + "\n" +
                              "     Старший сержант - 10 дней" + "\n" +
                              "     Рыцарь - 14 дней" + "\n" +
                              "     Рыцарь-лейтенант - 21 день" + "\n" +
                              "     Рыцарь-капитан - 30 дней" + "\n" +
                              "     Рыцарь-защитник - 60 дней" + "\n" +
                              "     Чемпион Света - 90 дней" + "\n" +
                              "     Командор - 120 дней" + "\n" +
                              "     завоеватель - 150 дней" + "\n" +
                              "     Маршал - 180 дней" + "\n" +
                              "     Фельдмаршал - 240 дней" + "\n" +
                              "     Главнокомандующий - 300 дней" + "\n" +
                              "     Верховный воевода - 365 дней" + "\n" +
                              "     Бессмертный - 500 дней" + "\n" +
                              "Удачи! У вас всё получится!!!")


@bot.message_handler(commands=['start'])
def start(message):
    global user_id, cur, conn, now
    user_id = message.chat.id
    f = 0
    if if_user_in_the_db(user_id):
        f = 1
    # Если есть, бот игнорирует команду
    if f:
        pass
    # Если нет, бот добавляет пользователя в базу
    else:
        bot.send_message(user_id, 'СуперЖелезнаяВоля приветствует тебя, ' + message.chat.first_name + '! '
                         + 'Да начнётся побоище!')
        noww = str(now).split('.')[0]
        cur.execute("INSERT INTO users VALUES(?, ?, ?, ?)", (user_id, noww, 0, '-'))
        conn.commit()


# Удаление пользователя из БД
@bot.message_handler(commands=['end'])
def end(message):
    global user_id, cur, conn
    user_id = message.chat.id
    if if_user_in_the_db(user_id):
        bot.send_message(user_id, 'Ты зря сдаёшься! Сильнее ты, чем думаешь! Надеюсь, ты скоро вернёшься.')
        cur.execute("DELETE from users WHERE userid = ?", [(user_id)])
        conn.commit()


# Сколько дней держится человек
@bot.message_handler(commands=['getdays'])
def getdays(message):
    global user_id, cur, now
    user_id = message.chat.id
    # Просмотр информации о днях в БД
    cur.execute("SELECT * FROM users")
    all_results = cur.fetchall()
    for i in range(len(all_results)):
        if user_id in all_results[i]:
            n = all_results[i][2]
            # Если у человека 0 дней, то звание не даётся!
            if not n:
                bot.send_message(user_id, 'У тебя 0 дней.')
            # Если нет, то даётся определённое звание (информацию о них можно посмотреть в /info)
            else:
                bot.send_message(user_id, 'У тебя ' + str(n) + count(n) + '(' + all_results[i][3] + ')')


# Обнуление всех данных о пользователе
@bot.message_handler(commands=['restart'])
def restart(message):
    global user_id, cur, conn
    user_id = message.chat.id
    if if_user_in_the_db(user_id):
        bot.send_message(user_id, 'Не переживай! В следующий раз будет лучше!')
        noww = str(datetime.datetime.now()).split('.')[0]
        cur.execute("UPDATE users SET btime = ? WHERE userid = ?", (noww, user_id))
        cur.execute("UPDATE users SET days = ? WHERE userid = ?", (0, user_id))
        conn.commit()


# Установление нового времени начала 
@bot.message_handler(commands=['setstarttime'])
def setstartdate(message):
    global user_id, flag
    user_id = message.chat.id
    if if_user_in_the_db(user_id):
        # При введении команды, глобальная переменная flag становится True,
        # чтобы пользователь мог ответить на сообщение бота
        bot.send_message(user_id, 'Введи время начала: год, номер месяца, число, время' + '\n'
                         + '(гггг мм чч чч:мм). Например: 1970 01 01 00:00')
        flag = True


@bot.message_handler(content_types=['text'])
def setstartdate2(message):
    global user_id, cur, conn, flag, now
    user_id = message.chat.id
    try:
        # Если flag, то пользователь должен ввести время своего начала
        if flag:
            year = message.text.split()[0]
            month = message.text.split()[1]
            day = message.text.split()[2]
            hour = message.text.split()[3].split(':')[0]
            minute = message.text.split()[3].split(':')[1]
            # Время, введённое человеком превращается в переменную datetime
            d = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), 0)
            # Время, прошедшее с введённого начала до текущего времени
            delta = now - d
            # Если пользователь вводит время начала, которое раньше, чем текущее, то все хорошо
            if int(str(delta).split()[0]) > 0:
                cur.execute("UPDATE users SET btime = ? WHERE userid = ?", (str(d).split(',')[0], user_id))
                cur.execute("UPDATE users SET days = ? WHERE userid = ?", (int(str(delta).split()[0]), user_id))
                cur.execute("UPDATE users SET ach = ? WHERE userid = ?", (ach(str(delta).split()[0]), user_id))
                conn.commit()
                bot.send_message(user_id, 'Установлено новое время: ' + str(d).split(',')[0])
                flag = False
            # Если нет, то пользователь должен заново ввести данные
            else:
                bot.send_message(user_id,
                                 'Введи время начала: год, номер месяца, число, время' + '\n' + '(гггг мм чч чч:мм)')
    # Если пользователь ввёл дату не по образцу
    except IndexError:
        bot.send_message(user_id, 'Введи время начала: год, номер месяца, число, время' + '\n' + '(гггг мм чч чч:мм)')
    # Если у пользователя ошибки в дате (например: 30 февраля)
    except ValueError:
        bot.send_message(user_id, 'Введи время начала: год, номер месяца, число, время' + '\n' + '(гггг мм чч чч:мм)')
    # Если у пользователя лишние символы в сообщении
    except TypeError:
        bot.send_message(user_id, 'Введи время начала: год, номер месяца, число, время' + '\n' + '(гггг мм чч чч:мм)')


if __name__ == '__main__':
    bot.polling(none_stop=True)

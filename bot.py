import telebot
import sqlite3

bot = telebot.TeleBot("5436229582:AAHBayc_KAdkIFyHNuF4rDNgVaX7uXw_9H8", parse_mode=None)

count_galochka_Pasha = 0
users = ['/Pasha', '/Lesha', '/Dan', '/Artem', '/Dima', '/Ilia', '/Sania', '/Andey']
# user_id:   0         2        3        4         5       6         7         8;


# База данных
with sqlite3.connect("orders.db") as db:
    sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users(
           user_id INT PRIMARY KEY,
           count_checks INT);
        """)

def insert_varible_into_table(user_id, count_checks):
    global sql, db
    try:
        db = sqlite3.connect('orders.db')
        sql = db.cursor()

        db.execute("INSERT or IGNORE INTO users(user_id, count_checks) VALUES (?, ?)", (user_id, count_checks))
        db.commit()
        print(f"{user_id} {count_checks} вставлены в таблицу users")

        sql.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        sql.close()
        db.close()
        print("Соединение с SQLite закрыто")


def delete_sqlite_record(user_id):
    global sql, db
    try:
        db = sqlite3.connect('orders.db')
        sql = db.cursor()
        print("Подключен к SQLite")

        sql_update_query = """DELETE from users where user_id = ?"""
        sql.execute(sql_update_query, (user_id,))
        db.commit()
        print("Запись успешно удалена")
        sql.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        sql.close()
        db.close()
        print("Соединение с SQLite закрыто")


def print_db():
    global sql, db
    try:
        db = sqlite3.connect('orders.db')
        sql = db.cursor()
        print("Подключен к SQLite")

        for _ in sql.execute("SELECT * FROM users;"):
            print(sql.fetchall())

        sql.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        sql.close()
        db.close()
        print("Соединение с SQLite закрыто")


def check_user_in_db(user_id):
    global sql, db
    try:
        db = sqlite3.connect('orders.db')
        sql = db.cursor()

        info = sql.execute('SELECT * FROM users WHERE user_id=?', (user_id, ))
        if info.fetchone() is None:
            db.execute("INSERT INTO users(user_id) VALUES (?)", (user_id, ))
            db.commit()
            print('Добавил!')
        else:
            print(*sql.fetchall())
            print('None')

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        sql.close()
        db.close()
        print("Соединение с SQLite закрыто")


#delete_sqlite_record(i)
#insert_varible_into_table(8, 0)
#check_user_in_db(1)
#print_db()


# Функционал бота

@bot.message_handler(commands=['start'])
def start(message):
    print_name_person = f'{message.from_user.first_name}'
    bot.send_message(message.chat.id, f'Кому галочку начислить ?)')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f'По всем вопросам к кабану')

@bot.message_handler(commands=['stats'])
def stats(message):
    bot.send_message(message.chat.id, f'{message.from_user.first_name} {count_galochka_Pasha}')


@bot.message_handler(content_types=["text"])
def add(message):
    global users, count_galochka_Pasha
    print(message.text)
    if message.text in users:
        count_galochka_Pasha += 1
        bot.send_message(message.chat.id, f"Присвоил {message.from_user.first_name} галочку")
    else:
        print('Error')


bot.polling(none_stop=True)


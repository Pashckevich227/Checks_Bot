import telebot
import sqlite3

bot = telebot.TeleBot("5436229582:AAHBayc_KAdkIFyHNuF4rDNgVaX7uXw_9H8", parse_mode=None)

count_check_user = 0
users = ['/Pasha', '/Lesha', '/Dan', '/Artem', '/Dima', '/Ilia', '/Sania', '/Andey']
# user_id:   0         1        2        3         4       5         6         7;


# База данных
with sqlite3.connect("orders.db") as db:
    sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users(
           user_id INT PRIMARY KEY,
           count_checks INT);
        """)


def insert_variable_into_table(user_id, count_checks):
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


def print_all_db():
    global sql, db
    try:
        db = sqlite3.connect('orders.db')
        sql = db.cursor()
        print("Подключен к SQLite")

        for i in sql.execute("SELECT * FROM users;"):
            print(*i, sep=' ')

        sql.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        sql.close()
        db.close()
        print("Соединение с SQLite закрыто")


def print_checks_db(id_in_db):
    global sql, db, count_check_user
    try:
        db = sqlite3.connect('orders.db')
        sql = db.cursor()
        print("Подключен к SQLite")

        user_id = id_in_db
        checks = sql.execute("SELECT count_checks FROM users WHERE user_id = ?", (user_id,))
        count_check_user = checks.fetchone()
        print(*count_check_user)
        sql.close()
        return count_check_user[0]

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

        info = sql.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
        print(*info.fetchall())
        if info.fetchone() is None:
            db.execute("INSERT INTO users(user_id) VALUES (?)", (user_id,))
            db.commit()
            print('Добавил!')


    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        sql.close()
        db.close()
        print("Соединение с SQLite закрыто")


def update_sqlite_table(id_in_db):
    global sql, db
    try:
        db = sqlite3.connect('orders.db')
        sql = db.cursor()
        print("Подключен к SQLite")
        total = sql.execute("SELECT count_checks FROM users WHERE user_id = ?", (id_in_db,))
        upper_total = total.fetchone()[0] + 1
        print(upper_total)
        sql.execute(f"UPDATE users SET count_checks = {str(upper_total)} WHERE user_id = {id_in_db}")
        db.commit()
        print("Запись успешно обновлена")
        return sql.close() and db.commit()


    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        sql.close()
        db.close()
        print("Соединение с SQLite закрыто")


def reset(id_in_db):
    global sql, db
    try:
        db = sqlite3.connect('orders.db')
        sql = db.cursor()
        print("Подключен к SQLite")
        sql.execute(f"UPDATE users SET count_checks = 0 WHERE user_id = {id_in_db}")
        db.commit()
        print("Запись успешно обновлена")
        return sql.close() and db.commit()


    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        sql.close()
        db.close()
        print("Соединение с SQLite закрыто")


# delete_sqlite_record(0)
# insert_variable_into_table(8, 0)
# check_user_in_db(1)
#reset(7)
print_all_db()

# update_sqlite_table(0)

# for i in range(8):
#    update_sqlite_table(i, 0)

# print(count_check_user)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Кому галочку начислить ?)')


@bot.message_handler(commands=['help'])
def helping(message):
    bot.send_message(message.chat.id, f'По всем вопросам к кабану')


@bot.message_handler(commands=['stats'])
def stats(message):
    for i in range(8):
        bot.send_message(message.chat.id, str(users[i]) + f' {print_checks_db(str(i))}')


@bot.message_handler(content_types=["text"])
def add(message):
    global users, count_check_user
    if message.text in users:
        id_in_db = users.index(message.text)
        # print_checks_db(id_in_db)
        update_sqlite_table(id_in_db)
        bot.send_message(message.chat.id, f"Присвоил {users[id_in_db]} галочку")
    else:
        print('Error')


bot.polling(none_stop=True)

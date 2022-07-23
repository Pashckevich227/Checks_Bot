import telebot
import sqlite3

bot = telebot.TeleBot("5436229582:AAHBayc_KAdkIFyHNuF4rDNgVaX7uXw_9H8", parse_mode=None)

count_galochka_Pashckevich = 0

@bot.message_handler(commands=['start'])
def start(message):
    print_name_person = f'{message.from_user.first_name}'
    bot.send_message(message.chat.id, f'Кому галочку начислить ?)')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f'По всем вопросам к кабану')

@bot.message_handler(commands=['Галочку_Pashckevich'])
def add(message):
    global count_galochka_Pashckevich
    count_galochka_Pashckevich += 1
    bot.send_message(message.chat.id, f"Присвоил {message.from_user.first_name} галочку")

@bot.message_handler(commands=['stats'])
def stats(message):
    bot.send_message(message.chat.id, f'{message.from_user.first_name} {count_galochka_Pashckevich}')

bot.polling(none_stop=True)

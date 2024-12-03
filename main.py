import telebot
from db import Database
from telebot import types
import murkup as nav
import pandas as pd
import sqlite3
import os

bot = telebot.TeleBot("7529867595:AAEW9zXxj1OAC5F__o5PtX2qpJNDwdYiJ2k")

db = Database("database.db")


@bot.message_handler(commands=["start"])
def welcome(message):
    if not db.user_exists(message.chat.id):
        commands = [telebot.types.BotCommand("/start", "Перезапуск бота")]
        bot.set_my_commands(commands)
        db.add_user(message.chat.id)
        bot.send_message(message.chat.id, "Введите ФИО")
    elif db.get_nickname(message.chat.id) == "None":
        bot.send_message(message.chat.id, "Введите ФИО")
    else:
        panel(message.chat.id, "Вы уже зарегестрированы")


@bot.message_handler()
def bot_message(message):
    if not db.user_exists(message.chat.id):
        bot.send_message(message.chat.id, "напишите /start")


    elif message.text == "ПРОФИЛЬ":
         bot.send_message(message.chat.id, text="Вы зашли в профиль", reply_markup=types.ReplyKeyboardRemove(), parse_mode='Markdown')
         user_nickname = "Ваше ФИО: " + db.get_nickname(message.chat.id)
         bot.send_message(message.chat.id, user_nickname, reply_markup=nav.keyboard2)

    elif message.text == "НАЗАД":
        bot.send_message(message.chat.id, "Назад", reply_markup=nav.keyboard3)
        bot.delete_message(message.chat.id, message.message_id)

    elif message.text == "ДОБАВИТЬ МЕРОПРИЯТИЕ":
        if db.get_is_admin(message.chat.id) == "1":
            pass


    elif message.text == "АДМИН ПАНЕЛЬ":
        if db.get_is_admin(message.chat.id) == "1":
            bot.send_message(message.chat.id, "админ панель", reply_markup=nav.keyboard4)
            bot.delete_message(message.chat.id, message.message_id)
        else:
             panel(message.chat.id, "Вы не являетесь админом")


    elif message.text == "ПОЛУЧИТЬ ТАБЛИЦЫ":
        if db.get_is_admin(message.chat.id) == "1":
            try:
                os.remove("result.xlsx")
            except Exception:
                print("файл не был найден")
            conn = sqlite3.connect('database.db')
            df = pd.read_sql('select * from users', conn)
            df.to_excel(r'result.xlsx', index=False)
            bot.send_document(message.chat.id, open(r'result.xlsx', 'rb'))
            panel(message.chat.id, "Вам выданы таблицы")
        else:
             panel(message.chat.id, "Вы не являетесь админом")


    else:
        if db.get_signup(message.chat.id) == "setnickname":

            if len(message.text) > 60:
                bot.send_message(message.chat.id, "ФИО не должно быть больше 60 символов")
            elif "@" in message.text or "!" in message.text or "=" in message.text:
                bot.send_message(message.chat.id, "Вы ввели запрещенный символ")
            else:
                db.set_nickname(message.chat.id, message.text)
                db.set_signup(message.chat.id, "done")
                panel(message.chat.id, "Данные сохранены успешно")

        
        elif db.get_signup_admin(message.chat.id) == "installation":

            if message.text == "89677156771":
                db.set_is_admin(message.chat.id, True)
                panel(message.chat.id, "Вы стали админом")
                db.set_signup_admin(chat_id, "setadminpassword")
            else:
                db.set_signup_admin(message.chat.id, "setadminpassword")
                panel(message.chat.id, "Пароль неверный")


        else:
            bot.send_message(message.chat.id, "Некорректный ввод")


@bot.callback_query_handler(func=lambda call: call.data == 'change_data')
def save_btn(call):
    message = call.message
    chat_id = message.chat.id
    bot.send_message(chat_id, f'Изменение данных.')
    db.set_signup(message.chat.id, "setnickname")
    bot.send_message(chat_id, f'введите ФИО')

@bot.callback_query_handler(func=lambda call: call.data == 'admin_panel')
def activate_admin(call):
    message = call.message
    chat_id = message.chat.id
    if db.get_is_admin(chat_id) == "1":
        panel(message.chat.id, "Вы уже являетесь админом")
    else:
        bot.send_message(chat_id, f'Введите пароль')
        db.set_signup_admin(chat_id, "installation") 

@bot.callback_query_handler(func=lambda call: call.data == 'keyboard_back')
def back(call):
    message = call.message
    chat_id = message.chat.id
    panel(message.chat.id, "Назад")

def panel(chat_id, text):
    if db.get_is_admin(chat_id) == "1":
        bot.send_message(chat_id, text, reply_markup=nav.keyboard3)
    else: 
        bot.send_message(chat_id, text, reply_markup=nav.keyboard)


if __name__ == "__main__":
    print("Бот запущен!")
    bot.infinity_polling()

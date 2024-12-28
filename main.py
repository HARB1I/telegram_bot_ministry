import telebot
from db import Database
from telebot import types
import murkup as nav
import pandas as pd
from keyboa.keyboard import Keyboa
from config import Token, Admin_Password
import sqlite3
import os

bot = telebot.TeleBot(Token)

db = Database("database.db")

# ---------------------------------------------------------------------------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------------------------------------------------------------------------


@bot.message_handler()
def bot_message(message):
    match (message.text):

        # -------------------------------------------------------

        case "ПРОФИЛЬ":
            bot.send_message(message.chat.id, text="Вы зашли в профиль")
            user_nickname = "Ваше ФИО: " + db.get_nickname(message.chat.id)
            bot.send_message(message.chat.id, user_nickname, reply_markup=nav.keyboard2)

        # -------------------------------------------------------

        case "СПИСОК":
            if db.get_is_admin(message.chat.id) == "1":
                kb = db.get_topic_title()
                kb_topics = Keyboa(items=kb, items_in_row=2).keyboard
                bot.send_message(
                    message.chat.id, reply_markup=kb_topics, text="список мероприятий"
                )
            else:
                panel(message.chat.id, "Вы не являетесь админом")

        # -------------------------------------------------------

        case "НАЗАД":
            if db.get_is_admin(message.chat.id) == "1":
                bot.send_message(message.chat.id, "Назад", reply_markup=nav.keyboard3)
                bot.delete_message(message.chat.id, message.message_id)
            else:
                panel(message.chat.id, "Вы не являетесь админом")

        # -------------------------------------------------------

        case "МЕРОПРИЯТИЯ":  # для юзеров
            kb = db.get_topic_title()
            kb_topics = Keyboa(
                items=kb,
                copy_text_to_callback=True,
                front_marker="user_events|",
                items_in_row=2,
            ).keyboard
            bot.send_message(
                message.chat.id,
                reply_markup=kb_topics,
                text="выберите мероприятие на которое хотите оставить отзыв",
            )

        # -------------------------------------------------------

        case "МЕРOПРИЯТИЯ":  # буква O английская для админа
            if db.get_is_admin(message.chat.id) == "1":
                bot.send_message(
                    message.chat.id, reply_markup=nav.keyboard5, text="Мероприятия"
                )
                bot.delete_message(message.chat.id, message.message_id)
            else:
                panel(message.chat.id, "Вы не являетесь админом")

        # -------------------------------------------------------

        case "ДОБАВИТЬ":
            if db.get_is_admin(message.chat.id) == "1":
                bot.send_message(message.chat.id, text="Введите название мероприятия")
                db.set_flag_add_topic(message.chat.id, True)
            else:
                panel(message.chat.id, "Вы не являетесь админом")

        # -------------------------------------------------------

        case "АДМИН ПАНЕЛЬ":
            if db.get_is_admin(message.chat.id) == "1":
                bot.send_message(
                    message.chat.id, "админ панель", reply_markup=nav.keyboard4
                )
                bot.delete_message(message.chat.id, message.message_id)
            else:
                panel(message.chat.id, "Вы не являетесь админом")

        # -------------------------------------------------------

        case "ПОЛУЧИТЬ ТАБЛИЦЫ":
            if db.get_is_admin(message.chat.id) == "1":
                try:
                    os.remove("result.xlsx")
                except Exception:
                    print("файл не был найден")
                conn = sqlite3.connect("database.db")
                df = pd.read_sql("select * from users", conn)
                dx = pd.read_sql("select * from replies", conn)
                dv = pd.read_sql("select * from topic", conn)
                sales = pd.merge(df, dx, how="left", on="user_id")
                nh = pd.merge(dv, sales, how="left", on="topic_id")
                columns_to_remove = [
                    "signup",
                    "is_admin",
                    "signup_admin",
                    "flag_add_topic",
                    "is_content",
                    "n_content",
                    "id",
                ]
                nh = nh.drop(columns=columns_to_remove)
                nh.to_excel(r"result.xlsx", index=False)
                bot.send_document(message.chat.id, open(r"result.xlsx", "rb"))
                panel(message.chat.id, "Вам выданы таблицы")
            else:
                panel(message.chat.id, "Вы не являетесь админом")

        # -------------------------------------------------------

        case "УДАЛИТЬ":
            if db.get_is_admin(message.chat.id) == "1":
                kb = db.get_topic_title()
                kb_topics = Keyboa(
                    items=kb,
                    copy_text_to_callback=True,
                    front_marker="admin_delete|",
                    items_in_row=2,
                ).keyboard
                bot.send_message(
                    message.chat.id,
                    reply_markup=kb_topics,
                    text="выберите мероприятие которое хотите удалить",
                )
            else:
                panel(message.chat.id, "Вы не являетесь админом")

        # -------------------------------------------------------

        case _:
            if db.get_signup(message.chat.id) == "setnickname":

                if len(message.text) > 60:
                    bot.send_message(
                        message.chat.id, "ФИО не должно быть больше 60 символов"
                    )
                elif "@" in message.text or "!" in message.text or "=" in message.text:
                    bot.send_message(message.chat.id, "Вы ввели запрещенный символ")
                else:
                    db.set_nickname(message.chat.id, message.text)
                    db.set_signup(message.chat.id, "done")
                    panel(message.chat.id, "Данные сохранены успешно")

            # -------------------------------------------------------

            elif db.get_is_content(message.chat.id) == "1":
                if len(message.text) > 1000:
                    bot.send_message(
                        message.chat.id, "отзыв должен быть менее 1000 символов"
                    )
                else:
                    event = db.get_n_content(message.chat.id)
                    db.add_content(message.chat.id, event, message.text)
                    db.set_is_content(message.chat.id, False)
                    panel(message.chat.id, "отзыв успешно сохранен")

            # -------------------------------------------------------

            elif db.get_signup_admin(message.chat.id) == "installation":

                if message.text == Admin_Password:
                    db.set_is_admin(message.chat.id, True)
                    panel(message.chat.id, "Вы стали админом")
                    db.set_signup_admin(message.chat.id, "setadminpassword")
                else:
                    db.set_signup_admin(message.chat.id, "setadminpassword")
                    panel(message.chat.id, "Пароль неверный")

            # -------------------------------------------------------

            elif db.get_flag_add_topic(message.chat.id) == "1":
                db.set_flag_add_topic(message.chat.id, False)
                if len(message.text) > 60:
                    bot.send_message(
                        message.chat.id, "ФИО не должно быть больше 60 символов"
                    )
                elif "@" in message.text or "!" in message.text or "=" in message.text:
                    bot.send_message(message.chat.id, "Вы ввели запрещенный символ")
                else:
                    db.add_topic_title(message.text)
                    panel(message.chat.id, "новое мероприятие сохранено")

            # -------------------------------------------------------

            else:
                bot.send_message(message.chat.id, "Некорректный ввод")


# ---------------------------------------------------------------------------------------------------------------------------------------------


@bot.callback_query_handler(func=lambda call: True)
def save_btn(call):
    message = call.message
    chat_id = message.chat.id
    if call.data == "change_data":
        bot.send_message(chat_id, f"Изменение данных.")
        db.set_signup(message.chat.id, "setnickname")
        bot.send_message(chat_id, f"введите ФИО")

    # -------------------------------------------------------

    elif call.data == "admin_panel":
        if db.get_is_admin(chat_id) == "1":
            panel(message.chat.id, "Вы уже являетесь админом")
        else:
            bot.send_message(chat_id, f"Введите пароль")
            db.set_signup_admin(chat_id, "installation")

    # -------------------------------------------------------

    elif call.data == "keyboard_back":
        chat_id = message.chat.id
        panel(message.chat.id, "Назад")

    # -------------------------------------------------------

    elif call.data.split("|")[0] == "admin_delete":
        tp_id = db.get_topic_id(call.data.split("|")[1])
        db.delete_topic(tp_id)
        bot.send_message(
            message.chat.id, "мероприятие удалено", reply_markup=nav.keyboard3
        )

    # -------------------------------------------------------

    elif call.data.split("|")[0] == "user_events":
        event = db.get_topic_id(call.data.split("|")[1])
        db.set_is_content(message.chat.id, True)
        db.set_n_content(message.chat.id, event)
        bot.send_message(message.chat.id, "напишите отзыв о мероприятии")


# ---------------------------------------------------------------------------------------------------------------------------------------------


def panel(chat_id, text):
    if db.get_is_admin(chat_id) == "1":
        bot.send_message(chat_id, text, reply_markup=nav.keyboard3)
    else:
        bot.send_message(chat_id, text, reply_markup=nav.keyboard)


# ---------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    print("Бот запущен!")
    bot.infinity_polling()

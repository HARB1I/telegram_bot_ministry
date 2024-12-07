import telebot
from db import Database

db = Database("database.db")

#главное меню-----------------------------------------------------------------------------------------
button_save = telebot.types.InlineKeyboardButton(text="ПРОФИЛЬ")
button_save1 = telebot.types.InlineKeyboardButton(text="МЕРОПРИЯТИЯ")
keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add(button_save, button_save1)

#изменение имени--------------------------------------------------------------------------------------
button_change = telebot.types.InlineKeyboardButton("Изменить", callback_data='change_data')
button_admin = telebot.types.InlineKeyboardButton("admin", callback_data='admin_panel')
keyboard2 = telebot.types.InlineKeyboardMarkup(row_width=1).add(button_change, button_admin)

#главное меню админа--------------------------------------------------------------------------------------
button_save_admin = telebot.types.InlineKeyboardButton(text="ПРОФИЛЬ")
button_save1_admin = telebot.types.InlineKeyboardButton(text="МЕРОПРИЯТИЯ")
button_adminpanel = telebot.types.InlineKeyboardButton(text="АДМИН ПАНЕЛЬ")
keyboard3 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add(button_save_admin, button_save1_admin).add(button_adminpanel)

#админ панель----------------------------------------------------------------------------------------------
button_back1 = telebot.types.InlineKeyboardButton(text="НАЗАД")
exceel_file_get = telebot.types.InlineKeyboardButton(text="ПОЛУЧИТЬ ТАБЛИЦЫ")
add_event = telebot.types.InlineKeyboardButton(text="МЕРOПРИЯТИЯ") #буква O английская
keyboard4 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add(button_back1, exceel_file_get, add_event)

#добавление мероприятия------------------------------------------------------------------------------------
button_back = telebot.types.InlineKeyboardButton(text="НАЗАД")
button_add = telebot.types.InlineKeyboardButton(text="ДОБАВИТЬ")
button_delete = telebot.types.InlineKeyboardButton(text="УДАЛИТЬ")
button_list = telebot.types.InlineKeyboardButton(text="СПИСОК")
keyboard5 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add(button_back, button_list).add(button_add, button_delete)

#добавление мероприятия------------------------------------------------------------------------------------



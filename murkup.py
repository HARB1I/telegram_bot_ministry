import telebot

#главное меню-----------------------------------------------------------------------------------------
button_save = telebot.types.InlineKeyboardButton(text="ПРОФИЛЬ")
button_save1 = telebot.types.InlineKeyboardButton(text="НАПИСАТЬ О МЕРОПРИЯТИИ")
keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add(button_save, button_save1)

#изменение имени--------------------------------------------------------------------------------------
button_change = telebot.types.InlineKeyboardButton("Изменить", callback_data='change_data')
button_admin = telebot.types.InlineKeyboardButton("admin", callback_data='admin_panel')
button_back = telebot.types.InlineKeyboardButton("Назад", callback_data='keyboard_back')
keyboard2 = telebot.types.InlineKeyboardMarkup(row_width=1).add(button_change, button_admin, button_back)

#главное меню админа--------------------------------------------------------------------------------------
button_save_admin = telebot.types.InlineKeyboardButton(text="ПРОФИЛЬ")
button_save1_admin = telebot.types.InlineKeyboardButton(text="НАПИСАТЬ О МЕРОПРИЯТИИ")
button_adminpanel = telebot.types.InlineKeyboardButton(text="АДМИН ПАНЕЛЬ")
keyboard3 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add(button_save_admin, button_save1_admin).add(button_adminpanel)

#админ панель----------------------------------------------------------------------------------------------
button_back1 = telebot.types.InlineKeyboardButton(text="НАЗАД")
exceel_file_get = telebot.types.InlineKeyboardButton(text="ПОЛУЧИТЬ ТАБЛИЦЫ")
add_event = telebot.types.InlineKeyboardButton(text="ДОБАВИТЬ МЕРОПРИЯТИЕ")
keyboard4 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add(button_back1, exceel_file_get, add_event)

#выбор мероприятия------------------------------------------------------------------------------------

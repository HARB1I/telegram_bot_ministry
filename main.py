import telebot
from config import TOKEN
import sqlite3

bot = telebot.TeleBot(TOKEN)

#------------------------------------------------------------------------------------------------------------
@bot.message_handler(commands=['start'])
def welcome(message):
   chat_id = message.chat.id
   keyboard = telebot.types.ReplyKeyboardMarkup()
   button_save = telebot.types.InlineKeyboardButton(text="создать анкету")
   keyboard.add(button_save)
   bot.send_message(chat_id,'Добро пожаловать в бота сбора обратной связи',reply_markup=keyboard)


#------------------------------------------------------------------------------------------------------------
@bot.message_handler(func=lambda message: message.text == 'создать анкету')
def write_to_support(message):
   chat_id = message.chat.id
   bot.send_message(chat_id, 'Введите своё имя')
   bot.register_next_step_handler(message, save_username)


#------------------------------------------------------------------------------------------------------------
def save_username(message):
   db = sqlite3.connect('bot.db')
   c = db.cursor()

   chat_id = message.chat.id
   name = message.text
   #c.execute("DELETE FROM anketa WHERE user_id = (?)", (chat_id,))
   c.execute("INSERT INTO anketa (user_id) VALUES (?)", (chat_id,))

   c.execute("SELECT rowid FROM anketa WHERE user_id = (?) ORDER BY rowid DESC", (chat_id,))
   rowid = c.fetchone()[0]

   c.execute("UPDATE anketa SET username = (?1) WHERE user_id = (?2) AND rowid = (?3)", (name, chat_id, rowid))

   db.commit()
   db.close()

   bot.send_message(chat_id, f'Отлично, {name}. Теперь укажи свою фамилию')
   bot.register_next_step_handler(message, save_surname)

#------------------------------------------------------------------------------------------------------------
def save_surname(message):
   db = sqlite3.connect('bot.db')
   c = db.cursor()

   chat_id = message.chat.id
   surname = message.text

   c.execute("SELECT rowid FROM anketa WHERE user_id = (?) ORDER BY rowid DESC", (chat_id,))
   rowid = c.fetchone()[0]

   c.execute("UPDATE anketa SET surname = (?) WHERE (user_id = (?) AND rowid = (?))", (surname, chat_id, rowid))

   db.commit()
   db.close()
   
   bot.send_message(chat_id, f'Отлично, теперь расскажите свои впечатления о данном мероприятии')
   bot.register_next_step_handler(message, save_feedback)

#------------------------------------------------------------------------------------------------------------
def save_feedback(message):
   db = sqlite3.connect('bot.db')
   c = db.cursor()

   chat_id = message.chat.id
   feedback = message.text
   
   c.execute("SELECT rowid FROM anketa WHERE user_id = (?) ORDER BY rowid DESC", (chat_id,))
   rowid = c.fetchone()[0]

   c.execute("UPDATE anketa SET feedback = (?) WHERE (user_id = (?) AND rowid = (?))", (feedback, chat_id, rowid))

   db.commit()
   db.close()

   bot.send_message(chat_id, f'Спасибо за уделенное время')

#------------------------------------------------------------------------------------------------------------
@bot.message_handler(commands=['admin'])
def admin(message):
   chat_id = message.chat.id
   bot.send_message(chat_id, f'напишите пароль')
   bot.register_next_step_handler(message, echo_all)
   

#------------------------------------------------------------------------------------------------------------
def echo_all(message):
   chat_id = message.chat.id
   password = message.text
   if password == "123":
      bot.send_document(message.chat.id, open(r'bot.db', 'rb'))


#------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
   print('Бот запущен!')
   bot.infinity_polling()
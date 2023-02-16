from interface.CRUD import CRUD
import telebot
from telebot import types


token = '6098613911:AAG40OkVHWeWPTcnJbznaGsCTZbmBiFFFSY'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'hi'])
def start(message):
    mess = f'Привет, <b>{message.from_user.first_name}</b>, введите команду /data'
    bot.send_message(message.chat.id, mess, parse_mode='html')

op = ['Read', 'Create', 'Update', 'Delete']

@bot.message_handler(commands=['data'])
def data(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    markup.add(types.KeyboardButton('Read'))
    
    markup.add(types.KeyboardButton('Create'))

    markup.add(types.KeyboardButton('Update'))

    markup.add(types.KeyboardButton('Delete'))


    bot.send_message(message.chat.id, 'Кнопки для управление данными:', reply_markup=markup)

# @bot.callback_query_handler(func=lambda callback: callback.data == 'create')
# def bot_create(callback:types.CallbackQuery):
#     msg = bot.send_message

bot.polling(none_stop=True)


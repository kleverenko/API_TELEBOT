import telebot
from telebot import types
import json

from mixins import GetAllMixin, GetOneMixin, CreateMixin, UpdateMixin, DeleteMixin

class Interface(GetAllMixin,GetOneMixin, CreateMixin, UpdateMixin, DeleteMixin):
    pass

interface = Interface()

token = '6098613911:AAG40OkVHWeWPTcnJbznaGsCTZbmBiFFFSY'
bot = telebot.TeleBot(token)

HOST = 'http://3.67.196.232/'


inline_keyboard = types.InlineKeyboardMarkup()
inline_button = types.InlineKeyboardButton('просмотр', callback_data='readall')
inline_button2 = types.InlineKeyboardButton('создание', callback_data='create')
inline_button3 = types.InlineKeyboardButton('обновление', callback_data='update')
inline_button4 = types.InlineKeyboardButton('удаление', callback_data='delete')
inline_button5 = types.InlineKeyboardButton('просмотр по ID', callback_data='readone')
inline_button6 = types.InlineKeyboardButton('Остановить', callback_data='stop')

inline_keyboard.add(inline_button, inline_button5, inline_button2, inline_button3, inline_button4, inline_button6)



@bot.message_handler(commands=['start'])
def start(message: types.Message):
    bot.send_message(message.chat.id, f'Здравствуйте! {message.from_user.first_name, message.from_user.last_name}')
    bot.send_message(message.chat.id, 'Выбери действие: ', reply_markup=inline_keyboard)

def start2(message: types.Message):
    bot.send_message(message.chat.id, 'Выбери действие: ', reply_markup=inline_keyboard)



@bot.callback_query_handler(func=lambda callback: callback.data == 'readall')
def read_and_send_todo(callback: types.CallbackQuery):
    res = json.dumps(interface.get_all_todos(HOST), indent=4, ensure_ascii=False)
    bot.send_message(callback.message.chat.id, res)
    start2(callback.message)



@bot.callback_query_handler(func=lambda callback: callback.data == 'readone')
def read_one_todo(callback: types.CallbackQuery):
    msg = bot.send_message(callback.message.chat.id, 'Введите ID')
    bot.register_next_step_handler(msg, read_one)
def read_one(message):
    response = message.text
    result = json.dumps(interface.retrive_todo(HOST, response), indent=4, ensure_ascii=False)
    bot.send_message(message.chat.id, result)
    start2(message)




@bot.callback_query_handler(func=lambda callback: callback.data == 'create')
def create_new_todo(callback: types.CallbackQuery):
    mesg = bot.send_message(callback.message.chat.id, 
                            'Введите только название, если is_done = False\nВведите название и 1 через пробел если is_done = True')
    bot.register_next_step_handler(mesg, create_title)




def create_title(message):
    response = message.text
    res = response.split()
    if res[-1] != '1':
        result = interface.create_todo(HOST, ' '.join(res))
        if result == '1':
            bot.send_message(message.chat.id, 'Успешно создан')
            start2(message)
        elif result == '0':
            bot.send_message(message.chat.id, 'Ошибкочка')
            start2(message)
    elif res[-1] == '1':
        input_from_customer = response.split()

        result = interface.create_todo(HOST, ' '.join(res[:-1]), ''.join(res[-1]))
        if result == '1':
            bot.send_message(message.chat.id, 'Успешно создан')
            start2(message)
        elif result == '0':
            bot.send_message(message.chat.id, 'Ошибкочка')
            start2(message)




@bot.callback_query_handler(func=lambda callback: callback.data == 'update')
def update_todo_bot(callback: types.CallbackQuery):
    mesag = bot.send_message(callback.message.chat.id, 'Введите ID, и Название через пробел\n (Введите 1 через пробел в конце если is_done = True\nНе пишите ничего если is_done = False)')
    bot.register_next_step_handler(mesag, update_title)

def update_title(message):
    response = message.text.split()
    if response[-1] != '1':
        result = interface.update_todo(HOST, response[0], ' '.join(response[1:]))
        bot.send_message(message.chat.id, result)
        start2(message)
    elif response[-1] == '1':
        result = interface.update_todo(HOST, response[0], ' '.join(response[1:-1]), response[-1])
        bot.send_message(message.chat.id, result)
        start2(message)



 
@bot.callback_query_handler(func=lambda callback: callback.data == 'delete')
def delete_todo_bot(callback: types.CallbackQuery):
    res = json.dumps(interface.get_all_todos(HOST), indent=4, ensure_ascii=False)
    mesagee = bot.send_message(callback.message.chat.id, f'{res}\nВведите id который хотите удалить')
    bot.register_next_step_handler(mesagee, answer)

def answer(message):
    response = message.text
    result = interface.delete_todo(HOST, response)
    bot.send_message(message.chat.id, result)
    start2(message)
        



@bot.callback_query_handler(func=lambda callback: callback.data == 'stop')
def stopper(callback: types.CallbackQuery):
    bot.send_message(callback.message.chat.id, 'Досвидания')
    bot.stop_polling()


bot.polling()
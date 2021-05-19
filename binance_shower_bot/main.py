import telebot
from telebot import types
import telegram
import os
# import json
import re
import time
import random

from secure.tokens import TOKEN_TELEGRAM
from binance_api import Binance_view as B_view


TOKEN_TELEGRAM= TOKEN_TELEGRAM()    # TOKEN_TELEGRAM = '<Token Telegram Bot>'
bot = telebot.TeleBot(TOKEN_TELEGRAM)

class make_btn():
    def checkprices():
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        itembtn1 = types.KeyboardButton(text='Ціни на крипту')
        markup.add(itembtn1)
        return markup


@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    markup= make_btn.checkprices()
    bot.reply_to(message, f'Привєт пострижися, {message.from_user.first_name}', reply_markup=markup)

# @bot.message_handler(commands=['check'])
# def welcome(message):
#     bot.reply_to(message, f'Привєт пострижися, {message.from_user.first_name}')

def log_to_txt(log, file, path=''):
    f_path= str(path) + str(file)
    f= open(f_path, 'a', encoding='utf-8')  # UTF-8 обов'язково!
    f.write(log + '\n')
    f.close()

def log_messages(message):
    # print('=======\n',message, '\n=======\n')
    text= message.text
    user_id= message.from_user.id
    author= f"{message.from_user.first_name} {message.from_user.last_name} [{message.from_user.username}-{user_id}]"

    time_sms= time.ctime(message.date)
    
    log= f"{time_sms} - {author} : {text}"
    print('\n', log)
    log += f"  | json:{message}"
    log_to_txt(log, 'messages.txt')

# def send_mes(user_id, str):
#     return bot.send_message(user_id, str)

def get_prices(message, user_id=None, symbols=None):
    if symbols==None:
        result= B_view.view_prices()
        # print(result)
        # print('is not else', result)
    else:
        result= B_view.view_prices(symbols=symbols)
        # print('is else', result)
    
    prices= result['result']
    if user_id==None:
        user_id= message.from_user.id

    if result['status']:
        sms_return= 'Останні ціни на крипту:\n'
        for i in prices:
            for j in i:
                # print(j[0], j[1])
                sms_return += f"{j[0]} - {j[1]};\n"
            sms_return += '\n'
        bot.send_message(user_id, sms_return)
    else:
        print(user_id, 'api.binance.com не відповідає.\nЗанадто багато запитів за раз')
        bot.send_message(user_id, 'api.binance.com не відповідає')
        time.sleep(5)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    log_messages(message)
    user_id= message.from_user.id
    text= message.text
    try:
        text_int= int(text)
    except ValueError:
        text_int= False

    def re_search_in_arr(input_word, searched_words):
        for word in searched_words:
            if re.search(word, input_word.lower()):
                return True
        return False

    def make_symbols_local(text):
        symbols= B_view.take_symbol(text.upper())
        print('in main', symbols)
        return symbols


    markup= make_btn.checkprices()  # Клава

    hello_words= [r'привіт',r'здоров',r'хай']

    if re_search_in_arr(text, hello_words):
        bot.send_message(user_id, 'Привіт!', reply_markup=markup)
    elif text == 'Ціни на крипту':
        bot.send_message(user_id, 'Секунду...')
        bot.send_message(user_id, get_prices(message), reply_markup=markup)
    elif text == 'status':
        a= bot.get_updates()
        print('get_updates', a)
        b= bot.get_me()
        print('get_me', b)

    # Рандомайзер
    elif ('random' in text.lower()) or ('рандом' in text.lower()):
        ab= text.lower().split(' ')
        print('random', ab)
        try:
            a, b = ab[1], ab[2]
            if a.isdigit() and b.isdigit() and (int(a)<int(b)):
                res= random.randint(int(a), int(b))
                bot.send_message(user_id, f'Рандомне число між {a} та {b}:')
                bot.send_message(user_id, res, reply_markup=markup)
                print('answer: ', res)
            else:
                bot.send_message(user_id, 'Введіть коректно. Приклади:\nrandom 1 10\nрандом 22 100', reply_markup=markup)
        except IndexError:
            bot.send_message(user_id, 'Введіть коректно. Приклади:\nrandom 1 10\nрандом 22 100', reply_markup=markup)

    elif make_symbols_local(text):
        sym= make_symbols_local(text)
        bot.send_message(user_id, sym)
        bot.send_message(user_id, get_prices(message, symbols=sym), reply_markup=markup)
    else:
        bot.send_message(user_id, 'Я не поняв. Давай заново')
        bot.send_message(user_id, 'но на всяк...')
        bot.send_message(user_id, get_prices
    (message), reply_markup=markup)



bot.polling(none_stop=True)

test= {
    'content_type': 'text', 
    'id': 19, 
    'message_id': 19, 
    'from_user': {
        'id': 826760080, 
        'is_bot': False, 
        'first_name': 'Smuk', 
        'username': 'LerdoS1', 
        'last_name': 'Taras', 
        'language_code': 'uk', 
        'can_join_groups': None, 
        'can_read_all_group_messages': None, 
        'supports_inline_queries': None
        }, 
    'date': 1617319542, 
    'chat': {
        'id': 826760080, 
        'type': 'private', 
        'title': None, 
        'username': 'LerdoS1', 
        'first_name': 'Smuk', 
        'last_name': 'Taras', 
        'photo': None, 
        'bio': None, 
        'description': None, 
        'invite_link': None, 
        'pinned_message': None, 
        'permissions': None, 
        'slow_mode_delay': None, 
        'sticker_set_name': None, 
        'can_set_sticker_set': None, 
        'linked_chat_id': None, 
        'location': None
        },
    'forward_from': None, 
    'forward_from_chat': None, 
    'forward_from_message_id': None, 
    'forward_signature': None, 
    'forward_sender_name': None, 
    'forward_date': None, 
    'reply_to_message': None, 
    'edit_date': None, 
    'media_group_id': None, 
    'author_signature': None, 
    'text': 'gdfg', 
    'entities': None, 
    'caption_entities': None, 
    'audio': None, 
    'document': None, 
    'photo': None, 
    'sticker': None, 
    'video': None, 
    'video_note': None, 
    'voice': None, 
    'caption': None, 
    'contact': None, 
    'location': None, 
    'venue': None, 
    'animation': None, 
    'dice': None, 
    'new_chat_member': None, 
    'new_chat_members': None, 
    'left_chat_member': None, 
    'new_chat_title': None, 
    'new_chat_photo': None, 
    'delete_chat_photo': None, 
    'group_chat_created': None, 
    'supergroup_chat_created': None, 
    'channel_chat_created': None, 
    'migrate_to_chat_id': None, 
    'migrate_from_chat_id': None, 
    'pinned_message': None, 
    'invoice': None, 
    'successful_payment': None, 
    'connected_website': None, 
    'reply_markup': None, 
    'json': {
        'message_id': 19, 
        'from': {
            'id': 826760080, 
            'is_bot': False, 
            'first_name': 'Smuk', 
            'last_name': 'Taras', 
            'username': 'LerdoS1', 
            'language_code': 'uk'
            }, 
        'chat': {
            'id': 826760080, 
            'first_name': 'Smuk', 
            'last_name': 'Taras', 
            'username': 'LerdoS1', 
            'type': 'private'
            }, 
        'date': 1617319542, 
        'text': 'gdfg'
        }
}
test_bohdan= {
    'content_type': 'text', 
    'id': 225, 
    'message_id': 225, 
    'from_user': {
        'id': 805037677, 
        'is_bot': False, 
        'first_name': 'Bohdan', 
        'username': 'Easyk3', 
        'last_name': None, 
        'language_code': 'uk', 
        'can_join_groups': None, 
        'can_read_all_group_messages': None, 
        'supports_inline_queries': None
        }, 
    'date': 1618062480, 
    'chat': {
        'id': 805037677, 
        'type': 'private', 
        'title': None, 
        'username': 'Easyk3', 
        'first_name': 'Bohdan', 
        'last_name': None, 
        'photo': None, 
        'bio': None, 
        'description': None, 
        'invite_link': None, 
        'pinned_message': None, 
        'permissions': None, 
        'slow_mode_delay': None, 
        'sticker_set_name': None, 
        'can_set_sticker_set': None, 
        'linked_chat_id': None, 
        'location': None
        }, 
    'forward_from': None, 
    'forward_from_chat': None, 
    'forward_from_message_id': None, 
    'forward_signature': None, 
    'forward_sender_name': None, 
    'forward_date': None, 
    'reply_to_message': None, 
    'edit_date': None, 
    'media_group_id': None, 
    'author_signature': None, 
    'text': 'Ти є сам пдр', 
    'entities': None, 
    'caption_entities': None, 
    'audio': None, 
    'document': None, 
    'photo': None, 
    'sticker': None, 
    'video': None, 
    'video_note': None, 
    'voice': None, 
    'caption': None, 
    'contact': None, 
    'location': None, 
    'venue': None, 
    'animation': None, 
    'dice': None, 
    'new_chat_member': None, 
    'new_chat_members': None, 
    'left_chat_member': None, 
    'new_chat_title': None, 
    'new_chat_photo': None, 
    'delete_chat_photo': None, 
    'group_chat_created': None, 
    'supergroup_chat_created': None, 
    'channel_chat_created': None, 
    'migrate_to_chat_id': None, 
    'migrate_from_chat_id': None, 
    'pinned_message': None, 
    'invoice': None, 
    'successful_payment': None, 
    'connected_website': None, 
    'reply_markup': None, 
    'json': {
        'message_id': 225, 
        'from': {
            'id': 805037677, 
            'is_bot': False, 
            'first_name': 'Bohdan', 
            'username': 'Easyk3', 
            'language_code': 'uk'
            }, 
        'chat': {
            'id': 805037677, 
            'first_name': 'Bohdan', 
            'username': 'Easyk3', 
            'type': 'private'
            }, 
        'date': 1618062480, 
        'text': 'Ти є сам пдр'
        }
    }
# print(test['json']['text'])
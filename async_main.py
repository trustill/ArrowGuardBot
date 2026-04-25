import telebot
import asyncio
import config
import keyboards
import json
import db_actions

from telebot import types, logging
from telebot import TeleBot

telebot.telebot.logger.setLevel(logging.INFO)

bot = TeleBot(config.token)
db_client = db_actions.SqlQuery(config.conn_str)

with open("data_texts.json", encoding="utf-8") as file:
    msg_data = json.load(file)
with open("photos_url.json", encoding="utf-8") as file:
    images_url = json.load(file)

def accept_tou_menu(msg, lang):
    kb = keyboards.accept_tou_kb(lang)

    bot.send_message(chat_id=msg.chat.id,
                           text=msg_data[lang]["messages"]["accept_tou_menu"],
                           reply_markup=kb)

def welcome_message(msg, firstname=None):
    lang = db_client.get_user_lang(msg.chat.id)
    print(lang)
    username = firstname or "Anonymous"
    print(username)
    kb = keyboards.start_kb(lang)
    print(kb)

    tou_is_accept = db_client.is_accept_tou(msg.chat.id)
    print(tou_is_accept)

    if tou_is_accept:
        result_text = msg_data[lang]["messages"]["welcome_msg"].format(username=username)
        print(result_text)
        print(images_url["welcome_image"])

        send_photo_(msg.chat.id, images_url["welcome_image"], result_text, kb)
    else:
        accept_tou_menu(msg, lang)

def send_photo_(chat_id, photo_url=images_url["except_image"], text="Empty", kb=None):
    if chat_id != None:
        bot.send_photo(chat_id=chat_id,
                             photo=photo_url,
                             caption=text,
                             reply_markup=kb)
    else:
        print("Chat ID is empty")

@bot.message_handler(commands=["start"])
def start_conversation(msg):
    bot.send_message(msg.chat.id, "TEST")
    kb_choose_lang = keyboards.choose_language_kb()
    print(kb_choose_lang)
    bot.send_message(msg.chat.id, "TEST")
    try:
        client = db_client.get_user(msg.chat.id)
        print("CLIENT:", client)
    except Exception as e:
        print("DB ERROR:", e)
    bot.send_message(msg.chat.id, "TEST")

    if client:
        welcome_message(msg, msg.from_user.first_name)
    else:
        db_client.add_new_user(msg.chat.id)

        bot.send_message(chat_id=msg.chat.id,
                               text="Выберите язык:",
                               reply_markup=kb_choose_lang)

@bot.callback_query_handler(func=lambda x: x.data.startswith('change_lang_to_ru'))
def change_lang_ru(query):
    user_id = query.message.chat.id
    lang = db_client.get_user_lang(user_id)

    bot.delete_message(chat_id=user_id,
                             message_id=query.message.id)

    if lang == None:
        db_client.change_user_lang(user_id, "russian")
        welcome_message(query.message, query.from_user.first_name)
    else:
        db_client.change_user_lang(user_id, "russian")

        bot.send_message(chat_id=user_id,
                               text="Ваш язык успешно изменен на русский!")

@bot.callback_query_handler(func=lambda x: x.data.startswith('change_lang_to_eng'))
def change_lang_eng(query):
    user_id = query.message.chat.id
    lang = db_client.get_user_lang(user_id)

    bot.delete_message(chat_id=user_id,
                             message_id=query.message.id)

    if lang == None:
        db_client.change_user_lang(user_id, "english")
        welcome_message(query.message, query.from_user.first_name)
    else:
        db_client.change_user_lang(user_id, "english")

        bot.send_message(chat_id=user_id,
                               text="Your language has been successfully changed to English!")

@bot.callback_query_handler(func=lambda x: x.data.startswith('account'))
def account_menu(query):
    user_id = query.message.chat.id
    lang = db_client.get_user_lang(user_id)


@bot.callback_query_handler(func=lambda x: x.data.startswith('accept_tou'))
def user_accepted_tou(query):
    db_client.change_tou_status(True, query.message.chat.id)

    welcome_message(query.message, query.from_user.first_name)
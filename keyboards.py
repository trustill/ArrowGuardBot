from telebot import types
import json

with open("data_texts.json", "r", encoding="utf-8") as file:
    msg_data = json.load(file)

def choose_language_kb():
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text="Русский 🇷🇺", callback_data="change_lang_to_ru"),
        types.InlineKeyboardButton(text="English 🇬🇧", callback_data="change_lang_to_eng")
    )

def start_kb(lang):
    return types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton(text=msg_data[lang]["buttons"]["try_free"], callback_data="try_free"),
        types.InlineKeyboardButton(text=msg_data[lang]["buttons"]["subscribe"], callback_data="subscribe"),
        types.InlineKeyboardButton(text=msg_data[lang]["buttons"]["account"], callback_data="account")
    )

def accept_tou_kb(lang):
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text=msg_data[lang]["buttons"]["accept_tou"], callback_data="accept_tou"))

def account_kb(lang):
    return types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton(text=msg_data[lang]["buttons"]["try_free"], callback_data="try_free"),
        types.InlineKeyboardButton(text=msg_data[lang]["buttons"]["subscribe"], callback_data="subscribe"),
        types.InlineKeyboardButton(text=msg_data[lang]["buttons"]["my_key"], callback_data="my_key"),
        types.InlineKeyboardButton(text=msg_data[lang]["buttons"]["support"], callback_data="support"),
    )
def get_plans(lang):
    return types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton(text=msg_data[lang]["buttons"]["one_month"], callback_data="sub:1month"),
        types.InlineKeyboardButton(text=msg_data[lang]["buttons"]["three_month"], callback_data="sub:3month"),
        types.InlineKeyboardButton(text=msg_data[lang]["buttons"]["one_year"], callback_data="sub:1year"),
        types.InlineKeyboardButton(text=msg_data[lang]["buttons"]["back"], callback_data="back:menu")
    )

def back_kb(lang):
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton(text=msg_data[lang]["buttons"]["back"], callback_data="back:menu"))

def my_key_kb(lang):
    return types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton(text=msg_data[lang]["buttons"]["key_url"], url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
        types.InlineKeyboardButton(text=msg_data[lang]["buttons"]["instructions"], callback_data="instructions"),
        types.InlineKeyboardButton(text=msg_data[lang]["buttons"]["back"], callback_data="back:menu"))

def pay_kb(lang, user_id):
    return types.InlineKeyboardMarkup(row_width=1).add(
        types.InlineKeyboardButton(text=msg_data[lang]["buttons"]["pay"], url=f"https://arrowguardbot.onrender.com/pay?user_id={user_id}"),
    types.InlineKeyboardButton(text=msg_data[lang]["buttons"]["cancel_payment"], callback_data="back:plans"))